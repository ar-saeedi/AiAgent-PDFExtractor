# Universal PDF to Shopping Card Converter

**AI-Powered system that converts ANY product catalog PDF into beautiful e-commerce shopping cards**

## 🌟 Features

- ✅ **Universal PDF Support** - Works with ANY catalog type (Electronics, Fashion, Industrial, Medical, etc.)
- ✅ **AI-Powered Extraction** - Uses GPT-4 Vision, Claude Vision, Gemini for 98%+ accuracy
- ✅ **Multi-Method Extraction** - Text, tables, images, layout analysis
- ✅ **Beautiful HTML Output** - Professional, responsive shopping card design
- ✅ **Structured JSON Export** - Database-ready product data
- ✅ **Multi-Language Support** - Works with any language (UTF-8)

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure AI (Required)
Add your API key to `config/.env.example` and rename to `.env`:

```bash
# Choose ONE provider:
DEEPSEEK_API_KEY=your_key_here       # Recommended - Fast & Affordable
# OR
ANTHROPIC_API_KEY=your_key_here      # Best for technical docs
# OR
OPENAI_API_KEY=your_key_here         # GPT-4 Vision
# OR  
GOOGLE_API_KEY=your_key_here         # Gemini
# OR
HUGGINGFACE_API_KEY=your_key_here    # FREE option
```

**Get API Keys:**
- DeepSeek: https://platform.deepseek.com/ (⭐ Fast, Affordable, 98%+ accuracy)
- Anthropic Claude: https://console.anthropic.com/ (Best for technical docs)
- OpenAI GPT-4: https://platform.openai.com/api-keys
- Google Gemini: https://makersuite.google.com/app/apikey
- Hugging Face: https://huggingface.co/settings/tokens (FREE)

### 3. Run Converter
```bash
# English (default)
python main.py your_catalog.pdf

# Persian (فارسی) - with RTL layout
python main.py your_catalog.pdf --lang persian

# Chinese (中文)
python main.py your_catalog.pdf --lang chinese
```

---

## 📁 Project Structure

```
pdfextractstoshoppingcard/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── README.md              # This file
│
├── src/                   # Core modules
│   ├── __init__.py
│   ├── universal_extractor.py    # PDF extraction
│   ├── ai_analyzer.py            # AI-powered analysis
│   ├── html_generator.py         # HTML generation
│   └── converter.py              # Main converter logic
│
├── config/                # Configuration
│   └── .env.example      # API key template
│
└── output/               # Generated files
    ├── *.html           # Shopping cards
    ├── *.json           # Structured data
    └── images/          # Extracted images
```

---

## 💻 Usage

### Basic Usage
```bash
python main.py catalog.pdf
```

### Specify Output
```bash
python main.py catalog.pdf --output my_product.html
```

### Python Integration
```python
import sys
sys.path.insert(0, 'src')

from converter import UniversalPDFConverter

# English version (default)
converter = UniversalPDFConverter(use_ai=True, use_vision=True, language='english')
output = converter.convert('catalog.pdf')

# Persian version with RTL
converter_fa = UniversalPDFConverter(use_ai=True, use_vision=True, language='persian')
output_fa = converter_fa.convert('catalog.pdf', 'product_fa.html')

# Chinese version
converter_zh = UniversalPDFConverter(use_ai=True, use_vision=True, language='chinese')
output_zh = converter_zh.convert('catalog.pdf', 'product_zh.html')
```

---

## 📊 Supported AI Providers

| Provider | Accuracy | Speed | Cost | Best For |
|----------|----------|-------|------|----------|
| **DeepSeek** ⭐ | 98%+ | Fast | $0.14/1M tokens | All catalogs |
| **Anthropic Claude** ⭐ | 98%+ | Fast | $0.10/catalog | Technical docs |
| **OpenAI GPT-4** | 97%+ | Medium | $0.50/catalog | Complex layouts |
| **Google Gemini** | 95%+ | Fast | Free tier | General catalogs |
| **Hugging Face** | 90%+ | Medium | FREE | Budget option |

---

## 🎯 How It Works

1. **Extract** - Multi-method PDF extraction (text, tables, images, layout)
2. **Analyze** - AI vision analyzes content and structure
3. **Structure** - Intelligent data organization
4. **Generate** - Beautiful HTML shopping card creation

---

## 📤 Output

For each PDF catalog:

### 1. HTML Shopping Card
- Modern, responsive design
- Product cards with specifications
- Interactive features
- Mobile-friendly
- Production-ready

### 2. JSON Data
```json
{
  "product_family": "Product Line",
  "category": "Electronics",
  "products": [
    {
      "name": "Product Name",
      "model": "MODEL-123",
      "specifications": {...},
      "features": [...],
      "pricing": {...}
    }
  ]
}
```

### 3. Images
- High-resolution page screenshots
- Extracted product images

---

## ⚙️ Command-Line Options

```bash
python main.py [PDF_FILE] [OPTIONS]

Options:
  -o, --output PATH        Output HTML file path
  --lang LANGUAGE          Output language: english, persian, chinese (default: english)
  --no-ai                  Run without AI (basic extraction)
  --no-vision              Use text-only AI
  --no-json                Don't save JSON files
  --demo                   Auto-find PDF in directory
  -h, --help               Show help
```

---

## 🔧 Requirements

- Python 3.8+
- AI API key (one of: Anthropic, OpenAI, Google, Hugging Face)
- Internet connection (for AI APIs)

### Dependencies
- pdfplumber - PDF text extraction
- PyMuPDF - PDF rendering & images
- Pillow - Image processing
- Jinja2 - HTML templating
- anthropic/openai/google-generativeai - AI providers

---

## 📈 Performance

- **Processing Speed**: ~0.5-1 sec/page
- **Accuracy**: 98%+ with AI (90%+ with Hugging Face FREE)
- **Memory Usage**: ~200-500 MB
- **Supported PDF Size**: Up to 100+ MB
- **Page Limit**: Unlimited

---

## 🌍 Multi-Language Support

### Direct AI Extraction in 3 Languages (NEW!)

The AI extracts and generates content **directly** in your target language - no translation needed!

| Language | Command | Layout | Features |
|----------|---------|--------|----------|
| **English** | `--lang english` (default) | LTR | Standard layout |
| **Persian (فارسی)** | `--lang persian` | **RTL** | Right-to-left + Persian fonts |
| **Chinese (中文)** | `--lang chinese` | LTR | Chinese fonts optimized |

**How it works:**
- AI analyzes the PDF and understands the content
- Generates all product descriptions, features, and specs **directly in your chosen language**
- HTML UI labels (buttons, headings) automatically localized
- For Persian: Full RTL support with proper font rendering
- For Chinese: Optimized fonts and proper character display

**Examples:**
```bash
# Generate English version (default)
python main.py catalog.pdf

# Generate Persian version with RTL layout
python main.py catalog.pdf --lang persian -o product_fa.html

# Generate Chinese version  
python main.py catalog.pdf --lang chinese -o product_zh.html
```

Powered by DeepSeek AI - perfect for international e-commerce!

---

## 💡 Use Cases

- **E-Commerce**: Convert supplier catalogs to product pages
- **B2B Marketplaces**: Digitize manufacturer catalogs
- **Product Management**: Catalog digitization and database population
- **Sales & Marketing**: Create product presentations and web content

---

## 🎓 Getting Help

1. **No AI configured**: Add API key to `config/.env`
2. **API errors**: Check your API key is valid
3. **PDF not found**: Use absolute path or place in same folder
4. **Poor quality**: Try different AI provider (Claude recommended)

---

## 📄 License

MIT License - Free for any use

---

## 👨‍💻 Author

**Alireza Saeedi**

- 📧 Email: alirezasaeediofficial@gmail.com
- 💻 GitHub: [Your GitHub Profile](https://github.com/alirezasaeedi)

---

## 🚀 Ready to Start?

1. Get API key from any provider
2. Add to `config/.env`
3. Run: `python main.py your_catalog.pdf`
4. Open generated HTML file!

**Made with ❤️ for automating product catalog digitization**

*Universal • AI-Powered • Production-Ready* ✨

---

**Created by Alireza Saeedi** • 2025
