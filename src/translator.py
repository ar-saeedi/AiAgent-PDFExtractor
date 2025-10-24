"""
AI-Powered Translator
Translates shopping cards to Persian and Chinese while preserving HTML structure
"""

import os
import sys
import json
from typing import Dict, Any
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

load_dotenv()


class AITranslator:
    """Translate product data using AI"""
    
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
    
    def translate_to_language(self, structured_data: Dict[str, Any], target_language: str) -> Dict[str, Any]:
        """Translate all text content to target language"""
        print(f"\n{'='*80}")
        print(f"AI TRANSLATOR - {target_language.upper()}")
        print(f"{'='*80}\n")
        
        if target_language.lower() == 'persian':
            return self._translate_to_persian(structured_data)
        elif target_language.lower() == 'chinese':
            return self._translate_to_chinese(structured_data)
        else:
            return structured_data
    
    def _translate_to_persian(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Translate to Persian (Farsi) using DeepSeek AI"""
        print("Translating to Persian (فارسی) using DeepSeek AI...")
        
        try:
            import requests
            
            data_to_translate = json.dumps(data, ensure_ascii=False, indent=2)
            
            API_URL = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            prompt = f"""Translate this product catalog JSON to Persian (Farsi). 
            
IMPORTANT:
- Translate ALL text values to Persian
- Keep JSON structure EXACTLY the same
- Keep all JSON keys in English (like "name", "model", "features", etc.)
- Translate ONLY the values (product names, descriptions, features, etc.)
- Return ONLY valid JSON, no markdown, no explanations

Original JSON:
{data_to_translate[:25000]}

Return the translated JSON:"""
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a professional Persian translator. Translate JSON values to Persian while keeping the structure intact. Return ONLY valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 8000,
                "temperature": 0.0
            }
            
            print("Sending to DeepSeek AI...")
            response = requests.post(API_URL, headers=headers, json=payload, timeout=180)
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    ai_response = result['choices'][0]['message']['content'].strip()
                    
                    import re
                    if '```json' in ai_response:
                        json_match = re.search(r'```json\s*(.*)\s*```', ai_response, re.DOTALL)
                        if json_match:
                            ai_response = json_match.group(1).strip()
                    elif '```' in ai_response:
                        json_match = re.search(r'```\s*(.*)\s*```', ai_response, re.DOTALL)
                        if json_match:
                            ai_response = json_match.group(1).strip()
                    
                    translated_data = json.loads(ai_response)
                    translated_data['_rtl'] = True
                    translated_data['_language'] = 'fa'
                    
                    print(f"✓ Persian translation complete! ({len(translated_data.get('products', []))} products)")
                    return translated_data
            
            print(f"Translation failed: {response.status_code}")
            data['_rtl'] = True
            data['_language'] = 'fa'
            return data
            
        except Exception as e:
            print(f"Translation error: {e}")
            data['_rtl'] = True
            data['_language'] = 'fa'
            return data
    
    def _translate_to_chinese(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Translate to Chinese using DeepSeek AI"""
        print("Translating to Chinese (中文) using DeepSeek AI...")
        
        try:
            import requests
            
            data_to_translate = json.dumps(data, ensure_ascii=False, indent=2)
            
            API_URL = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            prompt = f"""Translate this product catalog JSON to Simplified Chinese (简体中文). 
            
IMPORTANT:
- Translate ALL text values to Chinese
- Keep JSON structure EXACTLY the same
- Keep all JSON keys in English (like "name", "model", "features", etc.)
- Translate ONLY the values (product names, descriptions, features, etc.)
- Return ONLY valid JSON, no markdown, no explanations

Original JSON:
{data_to_translate[:25000]}

Return the translated JSON:"""
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a professional Chinese translator. Translate JSON values to Simplified Chinese while keeping the structure intact. Return ONLY valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 8000,
                "temperature": 0.0
            }
            
            print("Sending to DeepSeek AI...")
            response = requests.post(API_URL, headers=headers, json=payload, timeout=180)
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    ai_response = result['choices'][0]['message']['content'].strip()
                    
                    import re
                    if '```json' in ai_response:
                        json_match = re.search(r'```json\s*(.*)\s*```', ai_response, re.DOTALL)
                        if json_match:
                            ai_response = json_match.group(1).strip()
                    elif '```' in ai_response:
                        json_match = re.search(r'```\s*(.*)\s*```', ai_response, re.DOTALL)
                        if json_match:
                            ai_response = json_match.group(1).strip()
                    
                    translated_data = json.loads(ai_response)
                    translated_data['_rtl'] = False
                    translated_data['_language'] = 'zh'
                    
                    print(f"✓ Chinese translation complete! ({len(translated_data.get('products', []))} products)")
                    return translated_data
            
            print(f"Translation failed: {response.status_code}")
            data['_rtl'] = False
            data['_language'] = 'zh'
            return data
            
        except Exception as e:
            print(f"Translation error: {e}")
            data['_rtl'] = False
            data['_language'] = 'zh'
            return data
    
    def _translate_text(self, text: str, target_lang: str) -> str:
        """Translate a single text string"""
        if not text or len(text.strip()) == 0:
            return text
        
        try:
            import requests
            
            API_URL = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": f"Translate this to {target_lang}: {text}\n\nReturn ONLY the translated text, nothing else."
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.0
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content'].strip()
            
            return text
            
        except:
            return text
    
    def _call_translation_api(self, content: str, target_lang: str, instruction: str) -> Dict[str, Any]:
        """Call DeepSeek API for translation"""
        try:
            import requests
            
            prompt = f"""{instruction}

Source JSON (in English):
{content[:20000]}

Return the same JSON structure with all text values translated to {target_lang}. Keep all JSON keys in English. Translate only the values.
Return ONLY valid JSON, no other text."""

            API_URL = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are a professional translator. Translate to {target_lang} accurately. Return ONLY valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 8000,
                "temperature": 0.0
            }
            
            print(f"Sending to DeepSeek for {target_lang} translation...")
            response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    ai_response = result['choices'][0]['message']['content'].strip()
                    
                    import re
                    if '```json' in ai_response:
                        json_match = re.search(r'```json\s*(.*?)\s*```', ai_response, re.DOTALL)
                        if json_match:
                            ai_response = json_match.group(1).strip()
                    elif '```' in ai_response:
                        json_match = re.search(r'```\s*(.*?)\s*```', ai_response, re.DOTALL)
                        if json_match:
                            ai_response = json_match.group(1).strip()
                    
                    try:
                        translated_data = json.loads(ai_response)
                        return translated_data
                    except json.JSONDecodeError as e:
                        print(f"Translation JSON error: {str(e)[:100]}")
                        print(f"Trying to fix...")
                        ai_response = re.sub(r',\s*}', '}', ai_response)
                        ai_response = re.sub(r',\s*]', ']', ai_response)
                        translated_data = json.loads(ai_response)
                        return translated_data
            
            print(f"Translation error: {response.status_code}")
            return None
            
        except Exception as e:
            print(f"Translation error: {e}")
            return None

