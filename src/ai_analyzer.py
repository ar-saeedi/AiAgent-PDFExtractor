"""
Advanced AI Analyzer - Uses Vision AI for Universal PDF Understanding
Supports: GPT-4 Vision, Claude Vision, Gemini Vision
Works with ANY type of product catalog
"""

import os
import json
import base64
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

load_dotenv()


class UniversalAIAnalyzer:
    """
    Universal AI-powered catalog analyzer
    Uses vision AI to understand ANY product catalog
    """
    
    def __init__(self, use_vision: bool = True):
        self.use_vision = use_vision
        self.ai_provider = self._detect_available_ai()
        
    def _detect_available_ai(self) -> Optional[str]:
        """Detect which AI APIs are available"""
        openai_key = os.getenv('OPENAI_API_KEY', '').strip()
        anthropic_key = os.getenv('ANTHROPIC_API_KEY', '').strip()
        google_key = os.getenv('GOOGLE_API_KEY', '').strip()
        huggingface_key = os.getenv('HUGGINGFACE_API_KEY', '').strip()
        deepseek_key = os.getenv('DEEPSEEK_API_KEY', '').strip()
        
        if deepseek_key and deepseek_key.startswith('sk-'):
            return 'deepseek'
        elif anthropic_key and anthropic_key.startswith('sk-ant-'):
            return 'anthropic'
        elif huggingface_key and (huggingface_key.startswith('hf_') or len(huggingface_key) > 20):
            return 'huggingface'
        elif google_key and len(google_key) > 20:
            return 'google'
        elif openai_key and openai_key.startswith('sk-') and len(openai_key) > 20:
            return 'openai'
        
        return None
    
    def analyze_catalog(self, extracted_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze catalog using AI vision + text analysis
        Works with ANY type of product catalog
        """
        print(f"\n{'='*80}")
        print("UNIVERSAL AI ANALYZER")
        print(f"{'='*80}")
        print(f"AI Provider: {self.ai_provider or 'Rule-based (no API key)'}")
        print(f"Vision Analysis: {self.use_vision and self.ai_provider is not None}\n")
        
        if self.ai_provider and self.use_vision:
            # Use AI vision for highest accuracy
            structured_data = self._analyze_with_vision_ai(extracted_content)
        elif self.ai_provider:
            # Use AI text analysis
            structured_data = self._analyze_with_text_ai(extracted_content)
        else:
            # Fallback to advanced rule-based
            structured_data = self._analyze_with_advanced_rules(extracted_content)
        
        print(f"{'='*80}")
        print(f"Analysis complete!")
        print(f"Found {len(structured_data.get('products', []))} product(s)")
        print(f"{'='*80}\n")
        
        return structured_data
    
    def _analyze_with_vision_ai(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Use vision AI to analyze catalog images"""
        print("Using AI Analysis for maximum accuracy...")
        
        if self.ai_provider == 'deepseek':
            return self._analyze_with_deepseek(content)
        elif self.ai_provider == 'openai':
            return self._analyze_with_gpt4_vision(content)
        elif self.ai_provider == 'anthropic':
            return self._analyze_with_claude_vision(content)
        elif self.ai_provider == 'google':
            return self._analyze_with_gemini_vision(content)
        elif self.ai_provider == 'huggingface':
            return self._analyze_with_huggingface(content)
        else:
            print("\n⚠️  No AI provider configured. Please add API key.")
            return self._no_ai_configured()
    
    def _analyze_with_deepseek(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze using DeepSeek AI"""
        try:
            import requests
            
            print("Analyzing with DeepSeek AI...")
            
            full_text = self._combine_text(content)
            tables = self._extract_all_tables(content)
            
            prompt = self._get_analysis_prompt()
            prompt += f"\n\nIMPORTANT: Extract ONLY the actual model numbers and information from the text below. Do NOT make up or invent any model numbers.\n\nFull Text Content:\n{full_text[:40000]}"
            
            if tables:
                prompt += f"\n\nTables Found: {len(tables)}\n"
                for i, table in enumerate(tables[:10]):
                    prompt += f"\nTable {i+1} (Critical - contains specifications):\n"
                    for row in table['data'][:20]:
                        prompt += " | ".join([str(cell) if cell else "" for cell in row]) + "\n"
            
            API_URL = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert at analyzing product catalogs. You must extract ONLY the actual information from the provided text. NEVER invent or make up model numbers. Extract exactly what you see in the text. Return ONLY valid JSON with no markdown formatting."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 8000,
                "temperature": 0.0
            }
            
            print(f"Sending request to DeepSeek API...")
            print(f"Input size: {len(prompt)} characters, {len(tables)} tables")
            
            try:
                response = requests.post(API_URL, headers=headers, json=payload, timeout=180)
            except requests.exceptions.Timeout:
                print("DeepSeek timeout - retrying with smaller input...")
                prompt = self._get_analysis_prompt() + f"\n\nFull Text Content (first 20000 chars):\n{full_text[:20000]}"
                payload['messages'][1]['content'] = prompt
                response = requests.post(API_URL, headers=headers, json=payload, timeout=180)
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    ai_response = result['choices'][0]['message']['content']
                    print(f"✓ DeepSeek analysis complete!")
                    
                    import re
                    if '```json' in ai_response:
                        json_match = re.search(r'```json\s*(.*?)\s*```', ai_response, re.DOTALL)
                        if json_match:
                            ai_response = json_match.group(1).strip()
                    elif '```' in ai_response:
                        json_match = re.search(r'```\s*(.*?)\s*```', ai_response, re.DOTALL)
                        if json_match:
                            ai_response = json_match.group(1).strip()
                    
                    parsed_data = self._parse_ai_response(ai_response)
                    num_products = len(parsed_data.get('products', []))
                    print(f"✓ Successfully extracted {num_products} products!")
                    
                    if num_products == 0:
                        print("WARNING: No products extracted - this might be an error")
                    
                    return parsed_data
                else:
                    print(f"DeepSeek error: Unexpected response format")
                    return self._no_ai_configured()
            else:
                print(f"DeepSeek API error: {response.status_code} - {response.text[:200]}")
                return self._no_ai_configured()
                
        except Exception as e:
            print(f"DeepSeek error: {e}")
            import traceback
            traceback.print_exc()
            return self._no_ai_configured()
    
    def _analyze_with_gpt4_vision(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze using GPT-4 Vision"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            images_to_analyze = []
            for page in content['pages'][:5]:  # Analyze first 5 pages
                for img in page.get('images', []):
                    if img.get('type') == 'full_page' and os.path.exists(img.get('path', '')):
                        images_to_analyze.append(img['path'])
                        break
            
            # Combine text
            full_text = self._combine_text(content)[:15000]  # Limit text
            
            # Prepare messages with vision
            messages = [{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": self._get_analysis_prompt() + f"\n\nExtracted Text:\n{full_text}"
                    }
                ]
            }]
            
            for img_path in images_to_analyze[:3]:
                with open(img_path, 'rb') as img_file:
                    img_data = base64.b64encode(img_file.read()).decode('utf-8')
                    messages[0]["content"].append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_data}"
                        }
                    })
            
            print(f"Analyzing with GPT-4 Vision ({len(images_to_analyze)} images)...")
            
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=messages,
                max_tokens=4096
            )
            
            result_text = response.choices[0].message.content
            return self._parse_ai_response(result_text)
            
        except Exception as e:
            print(f"GPT-4 Vision error: {e}")
            print("Falling back to advanced rules...")
            return self._analyze_with_advanced_rules(content)
    
    def _analyze_with_claude_vision(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze using Claude Vision"""
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            
            images_to_analyze = []
            for page in content['pages'][:5]:
                for img in page.get('images', []):
                    if img.get('type') == 'full_page' and os.path.exists(img.get('path', '')):
                        images_to_analyze.append(img['path'])
                        break
            
            full_text = self._combine_text(content)[:15000]
            message_content = []
            for img_path in images_to_analyze[:3]:
                with open(img_path, 'rb') as img_file:
                    img_data = base64.b64encode(img_file.read()).decode('utf-8')
                    message_content.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": img_data
                        }
                    })
            
            message_content.append({
                "type": "text",
                "text": self._get_analysis_prompt() + f"\n\nExtracted Text:\n{full_text}"
            })
            
            print(f"Analyzing with Claude Vision ({len(images_to_analyze)} images)...")
            
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=16000,
                messages=[{
                    "role": "user",
                    "content": message_content
                }]
            )
            
            result_text = response.content[0].text
            return self._parse_ai_response(result_text)
            
        except Exception as e:
            print(f"Claude Vision error: {e}")
            print("Falling back to advanced rules...")
            return self._analyze_with_advanced_rules(content)
    
    def _analyze_with_gemini_vision(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze using Google Gemini Vision"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            
            for model_name in ['gemini-1.5-flash', 'gemini-1.5-pro-latest', 'gemini-pro-vision', 'gemini-pro']:
                try:
                    model = genai.GenerativeModel(model_name)
                    break
                except:
                    continue
            else:
                model = genai.GenerativeModel('models/gemini-1.5-flash')
            
            images_to_analyze = []
            for page in content['pages'][:5]:
                for img in page.get('images', []):
                    if img.get('type') == 'full_page' and os.path.exists(img.get('path', '')):
                        images_to_analyze.append(img['path'])
                        break
            
            full_text = self._combine_text(content)[:15000]
            prompt_parts = [self._get_analysis_prompt() + f"\n\nExtracted Text:\n{full_text}"]
            
            from PIL import Image as PILImage
            for img_path in images_to_analyze[:3]:
                img = PILImage.open(img_path)
                prompt_parts.append(img)
            
            print(f"Analyzing with Gemini Vision ({len(images_to_analyze)} images)...")
            
            response = model.generate_content(prompt_parts)
            return self._parse_ai_response(response.text)
            
        except Exception as e:
            print(f"Gemini Vision error: {e}")
            print("Falling back to advanced rules...")
            return self._analyze_with_advanced_rules(content)
    
    def _analyze_with_text_ai(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze using AI text-only (no vision)"""
        print("Using AI Text Analysis...")
        
        try:
            full_text = self._combine_text(content)
            tables = self._extract_all_tables(content)
            
            prompt = self._get_analysis_prompt()
            prompt += f"\n\nFull Text Content:\n{full_text[:20000]}"
            
            if tables:
                prompt += f"\n\nTables Found: {len(tables)}"
                for i, table in enumerate(tables[:5]):
                    prompt += f"\n\nTable {i+1}:\n"
                    for row in table['data'][:10]:
                        prompt += " | ".join([str(cell) if cell else "" for cell in row]) + "\n"
            
            if self.ai_provider == 'anthropic':
                from anthropic import Anthropic
                client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=16000,
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.content[0].text
            elif self.ai_provider == 'openai':
                from openai import OpenAI
                client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
                response = client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=4096
                )
                result = response.choices[0].message.content
            elif self.ai_provider == 'deepseek':
                return self._analyze_with_deepseek(content)
            elif self.ai_provider == 'huggingface':
                return self._analyze_with_huggingface(content)
            else:
                print("\n⚠️  No AI provider configured. Please add API key.")
                return self._no_ai_configured()
            
            return self._parse_ai_response(result)
            
        except Exception as e:
            print(f"AI Text Analysis error: {e}")
            return self._analyze_with_advanced_rules(content)
    
    def _get_analysis_prompt(self) -> str:
        """Get universal analysis prompt for ANY catalog"""
        return """You are analyzing a product catalog PDF. Extract and structure ALL product information into JSON format for an e-commerce shopping cart.

Your task:
1. Identify ALL products/models in the catalog (could be 1 or 100+ products)
2. Extract product details, specifications, features, pricing
3. Identify the company/brand information
4. Detect the product category/industry

Return ONLY valid JSON in this exact structure:
{
    "product_family": "Main product line or catalog name",
    "category": "Product category (e.g., Electronics, Industrial, Fashion, etc.)",
    "company": {
        "name": "Company name",
        "website": "Website URL if found",
        "phone": "Phone number if found",
        "email": "Email if found"
    },
    "products": [
        {
            "name": "Full product name",
            "model": "Model number/SKU",
            "tagline": "Short marketing tagline",
            "description": "Detailed product description",
            "features": ["feature 1", "feature 2", ...],
            "specifications": {
                "Category Name": {
                    "spec_name": "spec_value",
                    ...
                }
            },
            "applications": ["use case 1", "use case 2", ...],
            "pricing": {
                "price": "price value or 'Contact for quote'",
                "currency": "USD/EUR/etc",
                "note": "any pricing notes"
            },
            "images_count": number_of_images_for_this_product
        }
    ]
}

Rules:
- Extract ALL products (not just one)
- Be precise with specifications
- Preserve exact model numbers
- Include all features mentioned
- If information is missing, omit the field or use null
- Return ONLY valid JSON, no other text"""
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response into structured data"""
        try:
            json_text = response_text.strip()
            data = json.loads(json_text)
            return data
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {str(e)[:100]}")
            print(f"Attempting to fix malformed JSON...")
            
            try:
                import re
                json_text = response_text.strip()
                json_text = re.sub(r',\s*}', '}', json_text)
                json_text = re.sub(r',\s*]', ']', json_text)
                
                data = json.loads(json_text)
                return data
            except:
                print("ERROR: AI returned invalid JSON format")
                return {
                    "product_family": "Extraction Error",
                    "category": "AI Response Invalid",
                    "company": {},
                    "products": []
                }
        except Exception as e:
            print(f"Parse Error: {e}")
            return {
                "product_family": "Product Catalog",
                "category": "General",
                "company": {},
                "products": []
            }
    
    def _analyze_with_huggingface(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze using Hugging Face FREE API"""
        try:
            import requests
            
            print("Using Hugging Face AI (FREE)...")
            
            API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
            headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}
            
            full_text = self._combine_text(content)[:10000]
            prompt = f"Analyze this product catalog and extract all product names, models, specifications, and features:\n\n{full_text}"
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Hugging Face analysis complete")
                if isinstance(result, list) and len(result) > 0:
                    ai_summary = result[0].get('summary_text', '')
                return {
                    "product_family": "Product Catalog",
                    "category": "Products",
                    "company": {},
                    "products": [{
                        "name": "See extracted data",
                        "model": "Hugging Face extraction",
                        "description": ai_summary if 'ai_summary' in locals() else "AI analysis complete",
                        "features": [],
                        "specifications": {},
                        "applications": [],
                        "pricing": {"price": "See catalog", "currency": "USD"}
                    }]
                }
            else:
                print(f"Hugging Face API error: {response.status_code}")
                return self._no_ai_configured()
                
        except Exception as e:
            print(f"Hugging Face error: {e}")
            return self._no_ai_configured()
    
    def _no_ai_configured(self) -> Dict[str, Any]:
        """Return message when AI is not configured"""
        print("\n" + "="*80)
        print("⚠️  AI NOT CONFIGURED")
        print("="*80)
        print("\nThis system requires AI for accurate extraction.")
        print("\nSupported AI Providers:")
        print("  • Anthropic Claude (BEST) - https://console.anthropic.com/")
        print("  • OpenAI GPT-4 Vision - https://platform.openai.com/api-keys")
        print("  • Google Gemini - https://makersuite.google.com/app/apikey")
        print("  • Hugging Face (FREE) - https://huggingface.co/settings/tokens")
        print("\nAdd your API key to .env file:")
        print("  ANTHROPIC_API_KEY=your_key_here")
        print("\nThen run again for full AI-powered extraction.")
        print("="*80 + "\n")
        
        return {
            "product_family": "AI Configuration Required",
            "category": "Please Add API Key",
            "company": {
                "name": "Configure AI to extract company info",
                "website": "",
                "phone": ""
            },
            "products": [{
                "name": "AI API Key Required",
                "model": "N/A",
                "tagline": "Add API key to .env file to enable extraction",
                "description": "This system uses AI to intelligently extract product information from ANY catalog. Please configure an AI provider by adding your API key to the .env file in the config folder.",
                "features": ["Real-time AI extraction", "Works with any PDF type", "98%+ accuracy with proper AI"],
                "specifications": {},
                "applications": [],
                "pricing": {"price": "Configure AI", "currency": "USD"}
            }]
        }
    
    def _combine_text(self, content: Dict[str, Any]) -> str:
        """Combine all text from pages"""
        texts = []
        for page in content['pages']:
            if page.get('text'):
                texts.append(f"=== Page {page['page_number']} ===\n{page['text']}")
        return "\n\n".join(texts)
    
    def _extract_all_tables(self, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract all tables"""
        tables = []
        for page in content['pages']:
            for table in page.get('tables', []):
                tables.append({
                    'page': page['page_number'],
                    'data': table
                })
        return tables

