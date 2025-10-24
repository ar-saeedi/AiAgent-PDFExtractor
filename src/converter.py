"""
Universal PDF to Shopping Card Converter
Works with ANY type of product catalog
Professional, production-ready system
"""

import sys
import os
import json
from datetime import datetime
from typing import Optional, Dict
import argparse

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from universal_extractor import extract_pdf_universal
from ai_analyzer import UniversalAIAnalyzer
from html_generator import HTMLGenerator
from translator import AITranslator


class UniversalPDFConverter:
    """
    Universal PDF to Shopping Card Converter
    Works with ANY product catalog - Electronics, Fashion, Industrial, etc.
    """
    
    def __init__(self, use_ai: bool = True, use_vision: bool = True, language: str = 'english'):
        """
        Initialize converter
        
        Args:
            use_ai: Use AI for analysis (requires API key)
            use_vision: Use vision AI for image analysis (requires API key + vision models)
            language: Output language (english, persian, chinese)
        """
        self.use_ai = use_ai
        self.use_vision = use_vision
        self.language = language.lower()
        self.analyzer = UniversalAIAnalyzer(use_vision=use_vision)
        self.html_generator = HTMLGenerator()
        self.translator = AITranslator() if language.lower() in ['persian', 'chinese'] else None
    
    def convert(self, pdf_path: str, output_html: Optional[str] = None, 
                save_json: bool = True) -> str:
        """
        Convert any PDF catalog to shopping card
        
        Args:
            pdf_path: Path to PDF catalog file
            output_html: Output HTML path (auto-generated if None)
            save_json: Save intermediate JSON data
        
        Returns:
            Path to generated HTML file
        """
        print(f"\n{'='*80}")
        print("UNIVERSAL PDF TO SHOPPING CARD CONVERTER")
        print(f"{'='*80}")
        print(f"Input: {os.path.basename(pdf_path)}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"AI Enabled: {self.use_ai}")
        print(f"Vision AI: {self.use_vision and self.use_ai}")
        print(f"{'='*80}\n")
        
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        if output_html is None:
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            base_name = "".join(c for c in base_name if c.isalnum() or c in (' ', '-', '_'))
            base_name = base_name.strip()[:100]
            output_html = f"{base_name}_shopping_card.html"
        
        try:
            extracted = extract_pdf_universal(pdf_path)
            
            if save_json:
                extract_path = output_html.replace('.html', '_extracted.json')
                with open(extract_path, 'w', encoding='utf-8') as f:
                    json.dump(extracted, f, indent=2, ensure_ascii=False)
                print(f"✓ Saved extraction: {extract_path}\n")
            
            structured = self.analyzer.analyze_catalog(extracted)
            
            if self.translator and self.language in ['persian', 'chinese']:
                print(f"\n{'='*80}")
                print(f"TRANSLATING TO {self.language.upper()}")
                print(f"{'='*80}\n")
                structured = self.translator.translate_to_language(structured, self.language)
            
            if save_json:
                struct_path = output_html.replace('.html', '_data.json')
                with open(struct_path, 'w', encoding='utf-8') as f:
                    json.dump(structured, f, indent=2, ensure_ascii=False)
                print(f"✓ Saved structured data: {struct_path}\n")
            
                print(f"{'='*80}")
            print("GENERATING HTML SHOPPING CARD")
            print(f"{'='*80}\n")
            
            self.html_generator.generate(structured, output_html)
            
            # Summary
            self._print_summary(output_html, structured, pdf_path)
            
            return output_html
            
        except Exception as e:
            print(f"\n{'='*80}")
            print(f"ERROR: {e}")
            print(f"{'='*80}\n")
            import traceback
            traceback.print_exc()
            raise
    
    def _print_summary(self, output_html: str, structured: Dict, pdf_path: str):
        print(f"\n{'='*80}")
        print("CONVERSION COMPLETE!")
        print(f"{'='*80}\n")
        
        print(f"📄 Output HTML: {output_html}")
        print(f"📊 Product Family: {structured.get('product_family', 'N/A')}")
        print(f"🏷️  Category: {structured.get('category', 'N/A')}")
        print(f"🏢 Company: {structured.get('company', {}).get('name', 'N/A')}")
        print(f"🤖 Products Found: {len(structured.get('products', []))}")
        print(f"⏱️  Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        if structured.get('products'):
            print(f"{'='*80}")
            print("PRODUCTS EXTRACTED")
            print(f"{'='*80}\n")
            
            for i, product in enumerate(structured['products'][:10], 1):
                print(f"{i:2d}. {product.get('name', 'N/A')}")
                print(f"    Model: {product.get('model', 'N/A')}")
                print(f"    Features: {len(product.get('features', []))}")
                print(f"    Specs: {sum(len(v) if isinstance(v, dict) else 1 for v in product.get('specifications', {}).values())}")
                print()
            
            if len(structured['products']) > 10:
                print(f"    ... and {len(structured['products']) - 10} more products\n")
        
        print(f"{'='*80}")
        print(f"✅ Open {output_html} in your browser to view the shopping card!")
        print(f"{'='*80}\n")


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description='Universal PDF to Shopping Card Converter - Works with ANY catalog',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python converter.py catalog.pdf
  python converter.py catalog.pdf --output product.html
  python converter.py catalog.pdf --no-ai
  python converter.py catalog.pdf --no-vision
  python converter.py catalog.pdf --ai-only
        """
    )
    
    parser.add_argument('pdf_path', help='Path to PDF catalog file', nargs='?')
    parser.add_argument('-o', '--output', help='Output HTML file path')
    parser.add_argument('--no-ai', action='store_true', help='Disable AI analysis (use rules only)')
    parser.add_argument('--no-vision', action='store_true', help='Disable vision AI (use text AI only)')
    parser.add_argument('--ai-only', action='store_true', help='Use AI without vision')
    parser.add_argument('--no-json', action='store_true', help='Do not save intermediate JSON files')
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--lang', '--language', dest='language', default='english',
                       choices=['english', 'persian', 'chinese'],
                       help='Output language (english, persian, chinese)')
    
    args = parser.parse_args()
    
    if args.demo:
        import glob
        pdfs = glob.glob('*.pdf')
        if pdfs:
            args.pdf_path = pdfs[0]
            print(f"Demo mode: Processing {os.path.basename(args.pdf_path)}\n")
        else:
            print("Demo mode: No PDF files found in current directory.")
            return
    
    if not args.pdf_path:
        import glob
        pdfs = glob.glob('*.pdf')
        if pdfs:
            args.pdf_path = pdfs[0]
            print(f"Auto-detected PDF: {args.pdf_path}\n")
        else:
            print("Error: No PDF file specified and none found in current directory.")
            print("Usage: python converter.py <pdf_file>")
            sys.exit(1)
    
    use_ai = not args.no_ai
    use_vision = not args.no_vision and not args.ai_only
    language = args.language
    
    try:
        converter = UniversalPDFConverter(use_ai=use_ai, use_vision=use_vision, language=language)
        output = converter.convert(
            args.pdf_path,
            args.output,
            save_json=not args.no_json
        )
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\nConversion failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

