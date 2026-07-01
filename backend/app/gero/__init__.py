"""Gero — asistente IA de atención al cliente de OPTIMIZAR en WhatsApp.

Vive en WhatsApp (vía YCloud), tiene memoria en la base de datos, usa Anthropic
como cerebro interno (excepción documentada: tiempo real sobre webhook) y opera el
CRM: carga prospectos, los clasifica, les deja notas y agenda reuniones por Calendly.

Módulos:
- personalidad : el system prompt y la identidad de Gero.
- herramientas : las tools (function calling) que tocan el CRM.
- ycloud       : transporte de WhatsApp (enviar mensajes + parsear el webhook).
- cerebro      : el loop de conversación con Anthropic + memoria.
"""
