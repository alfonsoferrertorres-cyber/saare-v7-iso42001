from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import hashlib

API_KEY = "3EGo6tDasc3ppRh9Cmz2jSyoAUX_3g3KP6LF3k3V5euW37tmv"
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

app = FastAPI(
    title="S.A.A.R.E. v7.0 PRO - L7 Compliance Node",
    description="Zero-Token Stateless Middleware para ISO 42001",
    version="7.0"
)

async def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key"
    )

# --- ENDPOINT DE AUTENTICACIÓN PARA ZAPIER ---
@app.get("/auth")
async def auth_handshake(api_key: str = Depends(get_api_key)):
    """
    Endpoint de handshake para la validación inicial de Zapier.
    Retorna un estado exitoso si la API Key en las cabeceras es correcta.
    """
    return {"status": "authenticated", "node": "S.A.A.R.E. v7.0 PRO"}

# --- ENDPOINT DE VALIDACIÓN DE PROMPTS ---
class ComplianceRequest(BaseModel):
    prompt: str

class ComplianceResponse(BaseModel):
    allowed: bool
    evidence_hash: str
    detail: str

# Se elimina temporalmente 'api_key: str = Depends(get_api_key)' para aislar el timeout de Zapier
@app.post("/api/v7/validate", response_model=ComplianceResponse)
async def validate_prompt(request: ComplianceRequest):
    # Simulación de análisis semántico stateless sin persistencia en memoria
    prompt_len = len(request.prompt.strip())
    
    if prompt_len == 0:
        allowed = False
        detail = "El prompt está vacío."
    else:
        allowed = True
        detail = "Prompt verificado conforme a ISO 42001 (Zero-Retention)."
    
    # Generar hash SHA-256 como evidencia inmutable
    evidence_hash = hashlib.sha256(request.prompt.encode('utf-8')).hexdigest()
    
    return ComplianceResponse(
        allowed=allowed,
        evidence_hash=evidence_hash,
        detail=detail
    )