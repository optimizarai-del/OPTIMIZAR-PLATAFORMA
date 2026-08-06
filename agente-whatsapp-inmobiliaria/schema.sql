-- ============================================================
-- Agente WhatsApp Inmobiliaria Boutique — Schema Supabase
-- Bloque 1 · T01
-- Orden: properties → leads → agent_sessions (evita FK forward refs)
-- ============================================================

-- Habilitar extensión UUID (ya viene activa en Supabase)
create extension if not exists "pgcrypto";

-- Función de auto-update updated_at (definida antes de cualquier trigger)
create or replace function touch_updated_at()
returns trigger language plpgsql as $$
begin
    new.updated_at = now();
    return new;
end;
$$;

-- ------------------------------------------------------------
-- properties
-- Catálogo de propiedades de la inmobiliaria boutique.
-- El agente lo consulta para responder búsquedas.
-- Definida primero porque leads tiene FK a esta tabla.
-- ------------------------------------------------------------
create table if not exists properties (
    id              uuid primary key default gen_random_uuid(),
    codigo          text unique,                    -- código interno ej: DEP-001
    tipo            text not null,                  -- departamento / casa / oficina / local / terreno
    operacion       text not null,                  -- venta / alquiler
    titulo          text not null,
    descripcion     text,
    zona            text not null,
    barrio          text,
    direccion       text,
    superficie_total numeric(10,2),
    superficie_cubierta numeric(10,2),
    ambientes       integer,
    dormitorios     integer,
    banos           integer,
    cocheras        integer default 0,
    piso            integer,
    orientacion     text,
    amenities       jsonb default '[]',             -- ["pileta","gimnasio","sum"]
    precio          numeric(14,2) not null,
    moneda          text not null default 'USD',
    expensas        numeric(10,2),
    moneda_expensas text default 'ARS',
    fotos           jsonb default '[]',             -- URLs de fotos
    destacada       boolean not null default false,
    activa          boolean not null default true,
    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now()
);

create index if not exists idx_properties_tipo      on properties(tipo);
create index if not exists idx_properties_operacion on properties(operacion);
create index if not exists idx_properties_zona      on properties(zona);
create index if not exists idx_properties_activa    on properties(activa);
create index if not exists idx_properties_precio    on properties(precio);

drop trigger if exists trg_properties_updated_at on properties;
create trigger trg_properties_updated_at
    before update on properties
    for each row execute function touch_updated_at();

-- ------------------------------------------------------------
-- leads
-- Prospecto capturado por el agente WhatsApp.
-- Reutiliza la estructura de Oportunidad/Contacto del CRM
-- base pero simplificada para el flujo inmobiliario.
-- Definida antes de agent_sessions porque esta tiene FK a leads.
-- ------------------------------------------------------------
create table if not exists leads (
    id              uuid primary key default gen_random_uuid(),
    wa_phone        text not null,
    nombre          text,
    email           text,
    -- calificación
    tipo_operacion  text,                           -- compra / venta / alquiler
    tipo_propiedad  text,                           -- departamento / casa / oficina / local / terreno
    zona            text,
    presupuesto_min numeric(14,2),
    presupuesto_max numeric(14,2),
    moneda          text default 'USD',
    ambientes       integer,
    notas           text,                           -- texto libre del lead
    -- pipeline
    etapa           text not null default 'nuevo',  -- nuevo / calificado / visita_agendada / propuesta / cerrado / perdido
    fuente          text not null default 'whatsapp',
    -- visita agendada
    visita_fecha    timestamptz,
    visita_direccion text,
    property_id     uuid references properties(id) on delete set null,
    -- metadata
    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now()
);

create index if not exists idx_leads_phone  on leads(wa_phone);
create index if not exists idx_leads_etapa  on leads(etapa);
create index if not exists idx_leads_fuente on leads(fuente);

drop trigger if exists trg_leads_updated_at on leads;
create trigger trg_leads_updated_at
    before update on leads
    for each row execute function touch_updated_at();

-- ------------------------------------------------------------
-- agent_sessions
-- Contexto conversacional por número de WhatsApp.
-- Una fila por sesión activa; se crea al primer mensaje y
-- expira por TTL o cuando el lead convierte.
-- Definida última porque referencia leads.
-- ------------------------------------------------------------
create table if not exists agent_sessions (
    id              uuid primary key default gen_random_uuid(),
    wa_phone        text not null,                  -- número E.164 ej: +5491112345678
    constraint uq_agent_sessions_wa_phone unique (wa_phone),  -- target explícito para ON CONFLICT (wa_phone)
    lead_id         uuid references leads(id) on delete set null,
    messages        jsonb not null default '[]',    -- historial [{role, content, ts}]
    last_intent     text,                           -- última intención clasificada
    context         jsonb not null default '{}',    -- datos acumulados (zona, tipo_prop, etc.)
    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now(),
    expires_at      timestamptz not null default (now() + interval '24 hours')
);

create index if not exists idx_agent_sessions_phone on agent_sessions(wa_phone);
create index if not exists idx_agent_sessions_expires on agent_sessions(expires_at);

drop trigger if exists trg_sessions_updated_at on agent_sessions;
create trigger trg_sessions_updated_at
    before update on agent_sessions
    for each row execute function touch_updated_at();

-- ------------------------------------------------------------
-- RLS: habilitar Row Level Security
-- Acceso a leads y agent_sessions es EXCLUSIVO via service_role.
-- El service_role bypasea RLS automáticamente en Supabase, por lo que
-- las policies de abajo actúan como red de seguridad contra acceso anon directo.
-- Properties permite lectura pública de propiedades activas (portal web).
-- ------------------------------------------------------------
alter table agent_sessions enable row level security;
alter table leads           enable row level security;
alter table properties      enable row level security;

-- Bloqueo total para el rol anon en tablas sensibles.
-- Todo acceso legítimo ocurre con service_role (n8n, edge functions).
create policy "no anon access"
    on agent_sessions for all
    to anon
    using (false);

create policy "no anon access"
    on leads for all
    to anon
    using (false);

-- Service role bypasses RLS automáticamente en Supabase.
-- Policy pública solo para properties activas (el agente n8n usa service_role,
-- pero si algún cliente accede directo necesita esto).
create policy "properties_public_read"
    on properties for select
    using (activa = true);
