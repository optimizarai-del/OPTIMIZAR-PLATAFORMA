import os
import json
from datetime import datetime, timezone
from typing import Any
from supabase import create_client, Client

MAX_MESSAGES = 20
SESSION_TTL_HOURS = 24


def _supabase() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_KEY"]
    return create_client(url, key)


class SessionManager:
    """
    Maneja el contexto conversacional de una sesión WhatsApp en Supabase.

    Cada instancia es stateful para un wa_phone dado: carga la sesión al
    inicializarse y la persiste con save().

    Uso típico en n8n (Function node):
        sm = SessionManager(wa_phone)
        sm.add_message("user", incoming_text)
        intent_result = route_intent(incoming_text, sm.history_for_claude())
        sm.update_context(intent_result["extracted_data"])
        sm.last_intent = intent_result["intent"]
        reply = call_claude(sm.build_claude_payload())
        sm.add_message("assistant", reply)
        sm.save()
    """

    def __init__(self, wa_phone: str):
        self.wa_phone = wa_phone
        self.db = _supabase()
        self._row: dict | None = None
        self._load()

    # ── Carga / creación ──────────────────────────────────────────────────────

    def _load(self):
        res = (
            self.db.table("agent_sessions")
            .select("*")
            .eq("wa_phone", self.wa_phone)
            .single()
            .execute()
        )
        if res.data:
            row = res.data
            # Validar que la sesión no haya expirado.
            # Si expires_at <= NOW() se trata como sesión nueva: se descarta
            # historial y contexto previos para no contaminar la nueva conversación.
            # NOTA: las filas expiradas se acumulan en la tabla; agregar un job
            # de limpieza periódico via pg_cron:
            #   SELECT cron.schedule('purge_expired_sessions', '0 * * * *',
            #       $$DELETE FROM agent_sessions WHERE expires_at < now()$$);
            expires_raw = row.get("expires_at")
            if expires_raw:
                # Supabase devuelve el timestamp como string ISO 8601 con offset.
                expires_dt = datetime.fromisoformat(expires_raw)
                if expires_dt.tzinfo is None:
                    expires_dt = expires_dt.replace(tzinfo=timezone.utc)
                if expires_dt <= datetime.now(timezone.utc):
                    # Sesión expirada: iniciar conversación limpia reutilizando la fila.
                    self._row = row
                    self.reset()
                    return
            self._row = row
        else:
            self._row = self._create_session()

    def _create_session(self) -> dict:
        data = {
            "wa_phone": self.wa_phone,
            "messages": [],
            "context": {},
            "last_intent": None,
        }
        res = self.db.table("agent_sessions").insert(data).execute()
        return res.data[0]

    # ── Propiedades ───────────────────────────────────────────────────────────

    @property
    def session_id(self) -> str:
        return self._row["id"]

    @property
    def lead_id(self) -> str | None:
        return self._row.get("lead_id")

    @property
    def messages(self) -> list[dict]:
        msgs = self._row.get("messages") or []
        if isinstance(msgs, str):
            msgs = json.loads(msgs)
        return msgs

    @property
    def context(self) -> dict:
        ctx = self._row.get("context") or {}
        if isinstance(ctx, str):
            ctx = json.loads(ctx)
        return ctx

    @property
    def last_intent(self) -> str | None:
        return self._row.get("last_intent")

    @last_intent.setter
    def last_intent(self, value: str):
        self._row["last_intent"] = value

    # ── Mutaciones ────────────────────────────────────────────────────────────

    def add_message(self, role: str, content: str):
        """Agrega un mensaje al historial. Trunca al límite MAX_MESSAGES."""
        msgs = self.messages
        msgs.append({
            "role": role,
            "content": content,
            "ts": datetime.now(timezone.utc).isoformat(),
        })
        if len(msgs) > MAX_MESSAGES:
            msgs = msgs[-MAX_MESSAGES:]
        self._row["messages"] = msgs

    def update_context(self, data: dict[str, Any]):
        """Merge de datos extraídos de la intención al contexto acumulado."""
        ctx = self.context
        ctx.update({k: v for k, v in data.items() if v is not None})
        self._row["context"] = ctx

    def set_lead_id(self, lead_id: str):
        self._row["lead_id"] = lead_id

    # ── Claude payload ────────────────────────────────────────────────────────

    def history_for_claude(self) -> list[dict]:
        """
        Devuelve el historial en formato {role, content} para pasar a Claude.
        Filtra el campo 'ts' que Claude no necesita.
        Solo retorna los últimos MAX_MESSAGES mensajes.
        """
        return [
            {"role": m["role"], "content": m["content"]}
            for m in self.messages[-MAX_MESSAGES:]
        ]

    def build_claude_payload(self, system_prompt: str, new_user_message: str | None = None) -> dict:
        """
        Construye el payload completo para POST a /v1/messages de Claude.

        Si new_user_message se pasa, se agrega como último turno (útil cuando
        todavía no se llamó add_message para el turno actual).
        """
        history = self.history_for_claude()

        if new_user_message:
            history = history + [{"role": "user", "content": new_user_message}]

        # Si el historial empieza con un mensaje de assistant (no debería, pero
        # Claude requiere que el primer mensaje sea de user).
        if history and history[0]["role"] != "user":
            history = history[1:]

        return {
            "model": os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5"),
            "max_tokens": 1024,
            "system": system_prompt,
            "messages": history,
        }

    # ── Persistencia ──────────────────────────────────────────────────────────

    def save(self):
        """Persiste el estado actual en Supabase."""
        self.db.table("agent_sessions").update({
            "messages": self.messages,
            "context": self.context,
            "last_intent": self.last_intent,
            "lead_id": self.lead_id,
        }).eq("id", self.session_id).execute()

    def reset(self):
        """Limpia el historial y el contexto (nueva conversación con el mismo número)."""
        self._row["messages"] = []
        self._row["context"] = {}
        self._row["last_intent"] = None
        self.save()

    # ── Lead upsert ───────────────────────────────────────────────────────────

    def upsert_lead(self, data: dict) -> str:
        """
        Crea o actualiza el lead asociado a esta sesión.
        Devuelve el lead_id (UUID).

        data puede incluir: nombre, email, tipo_operacion, tipo_propiedad,
        zona, presupuesto_min, presupuesto_max, moneda, ambientes, notas, etapa.
        """
        if self.lead_id:
            self.db.table("leads").update(data).eq("id", self.lead_id).execute()
            return self.lead_id

        res = self.db.table("leads").insert({
            "wa_phone": self.wa_phone,
            **data,
        }).execute()
        lead_id = res.data[0]["id"]
        self.set_lead_id(lead_id)
        self.save()
        return lead_id
