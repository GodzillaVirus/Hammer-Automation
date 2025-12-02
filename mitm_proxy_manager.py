import asyncio
import json
import base64
from typing import Dict, List, Optional, Any
from mitmproxy import http, ctx
from mitmproxy.tools.main import mitmdump
from mitmproxy.options import Options
from mitmproxy.tools.dump import DumpMaster
import threading
import queue

class InterceptHandler:
    def __init__(self):
        self.requests = []
        self.responses = []
        self.intercept_rules = []
        self.modify_rules = []
        self.block_rules = []
        
    def request(self, flow: http.HTTPFlow) -> None:
        request_data = {
            "url": flow.request.url,
            "method": flow.request.method,
            "headers": dict(flow.request.headers),
            "content": base64.b64encode(flow.request.content).decode() if flow.request.content else None,
            "timestamp": flow.request.timestamp_start
        }
        self.requests.append(request_data)
        
        for rule in self.block_rules:
            if self._match_rule(flow.request, rule):
                flow.response = http.Response.make(403, b"Blocked by Hammer Automation")
                return
        
        for rule in self.modify_rules:
            if self._match_rule(flow.request, rule):
                self._apply_modifications(flow.request, rule)
    
    def response(self, flow: http.HTTPFlow) -> None:
        response_data = {
            "url": flow.request.url,
            "status_code": flow.response.status_code,
            "headers": dict(flow.response.headers),
            "content": base64.b64encode(flow.response.content).decode() if flow.response.content else None,
            "timestamp": flow.response.timestamp_start
        }
        self.responses.append(response_data)
        
        for rule in self.intercept_rules:
            if self._match_rule(flow.request, rule):
                if "response_modify" in rule:
                    self._modify_response(flow.response, rule["response_modify"])
    
    def _match_rule(self, request, rule):
        if "url_pattern" in rule:
            import re
            if not re.search(rule["url_pattern"], request.url):
                return False
        if "method" in rule:
            if request.method != rule["method"]:
                return False
        if "headers" in rule:
            for key, value in rule["headers"].items():
                if request.headers.get(key) != value:
                    return False
        return True
    
    def _apply_modifications(self, request, rule):
        if "headers" in rule.get("modify", {}):
            for key, value in rule["modify"]["headers"].items():
                request.headers[key] = value
        if "content" in rule.get("modify", {}):
            request.content = rule["modify"]["content"].encode()
    
    def _modify_response(self, response, modifications):
        if "status_code" in modifications:
            response.status_code = modifications["status_code"]
        if "headers" in modifications:
            for key, value in modifications["headers"].items():
                response.headers[key] = value
        if "content" in modifications:
            response.content = modifications["content"].encode()
    
    def add_intercept_rule(self, rule):
        self.intercept_rules.append(rule)
    
    def add_modify_rule(self, rule):
        self.modify_rules.append(rule)
    
    def add_block_rule(self, rule):
        self.block_rules.append(rule)
    
    def get_requests(self):
        return self.requests.copy()
    
    def get_responses(self):
        return self.responses.copy()
    
    def clear_history(self):
        self.requests.clear()
        self.responses.clear()

class MitmProxyManager:
    def __init__(self, port: int = 8080):
        self.port = port
        self.handler = InterceptHandler()
        self.master = None
        self.thread = None
        self.running = False
    
    def start(self):
        if self.running:
            return {"status": "already_running", "port": self.port}
        
        opts = Options(listen_host='0.0.0.0', listen_port=self.port)
        self.master = DumpMaster(opts)
        self.master.addons.add(self.handler)
        
        self.thread = threading.Thread(target=self._run_proxy, daemon=True)
        self.thread.start()
        self.running = True
        
        return {"status": "started", "port": self.port}
    
    def _run_proxy(self):
        try:
            asyncio.run(self.master.run())
        except Exception as e:
            ctx.log.error(f"Proxy error: {e}")
    
    def stop(self):
        if not self.running:
            return {"status": "not_running"}
        
        if self.master:
            self.master.shutdown()
        self.running = False
        
        return {"status": "stopped"}
    
    def add_intercept_rule(self, rule: Dict[str, Any]):
        self.handler.add_intercept_rule(rule)
        return {"status": "rule_added", "type": "intercept"}
    
    def add_modify_rule(self, rule: Dict[str, Any]):
        self.handler.add_modify_rule(rule)
        return {"status": "rule_added", "type": "modify"}
    
    def add_block_rule(self, rule: Dict[str, Any]):
        self.handler.add_block_rule(rule)
        return {"status": "rule_added", "type": "block"}
    
    def get_requests(self, limit: int = 100):
        requests = self.handler.get_requests()
        return requests[-limit:] if len(requests) > limit else requests
    
    def get_responses(self, limit: int = 100):
        responses = self.handler.get_responses()
        return responses[-limit:] if len(responses) > limit else responses
    
    def clear_history(self):
        self.handler.clear_history()
        return {"status": "cleared"}
    
    def get_status(self):
        return {
            "running": self.running,
            "port": self.port,
            "requests_count": len(self.handler.requests),
            "responses_count": len(self.handler.responses),
            "intercept_rules": len(self.handler.intercept_rules),
            "modify_rules": len(self.handler.modify_rules),
            "block_rules": len(self.handler.block_rules)
        }

proxy_manager = MitmProxyManager()
