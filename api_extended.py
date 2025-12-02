from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import logging

from mitm_proxy_manager import proxy_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mitm", tags=["MITM Proxy"])

class StartProxyRequest(BaseModel):
    port: int = 8080

class InterceptRuleRequest(BaseModel):
    url_pattern: Optional[str] = None
    method: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    response_modify: Optional[Dict[str, Any]] = None

class ModifyRuleRequest(BaseModel):
    url_pattern: Optional[str] = None
    method: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    modify: Optional[Dict[str, Any]] = None

class BlockRuleRequest(BaseModel):
    url_pattern: Optional[str] = None
    method: Optional[str] = None
    headers: Optional[Dict[str, str]] = None

@router.post("/start")
async def start_proxy(request: StartProxyRequest):
    try:
        result = proxy_manager.start()
        return result
    except Exception as e:
        logger.error(f"Failed to start proxy: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop")
async def stop_proxy():
    try:
        result = proxy_manager.stop()
        return result
    except Exception as e:
        logger.error(f"Failed to stop proxy: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_proxy_status():
    try:
        return proxy_manager.get_status()
    except Exception as e:
        logger.error(f"Failed to get proxy status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/intercept/add")
async def add_intercept_rule(rule: InterceptRuleRequest):
    try:
        result = proxy_manager.add_intercept_rule(rule.dict(exclude_none=True))
        return result
    except Exception as e:
        logger.error(f"Failed to add intercept rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/modify/add")
async def add_modify_rule(rule: ModifyRuleRequest):
    try:
        result = proxy_manager.add_modify_rule(rule.dict(exclude_none=True))
        return result
    except Exception as e:
        logger.error(f"Failed to add modify rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/block/add")
async def add_block_rule(rule: BlockRuleRequest):
    try:
        result = proxy_manager.add_block_rule(rule.dict(exclude_none=True))
        return result
    except Exception as e:
        logger.error(f"Failed to add block rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/requests")
async def get_intercepted_requests(limit: int = 100):
    try:
        return {"requests": proxy_manager.get_requests(limit)}
    except Exception as e:
        logger.error(f"Failed to get requests: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/responses")
async def get_intercepted_responses(limit: int = 100):
    try:
        return {"responses": proxy_manager.get_responses(limit)}
    except Exception as e:
        logger.error(f"Failed to get responses: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clear")
async def clear_history():
    try:
        return proxy_manager.clear_history()
    except Exception as e:
        logger.error(f"Failed to clear history: {e}")
        raise HTTPException(status_code=500, detail=str(e))
