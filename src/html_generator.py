"""
HTML Generator Module
Generates beautiful shopping card HTML from structured product data
"""

from jinja2 import Template
from typing import Dict, Any
import os
import json


class HTMLGenerator:
    """Generate e-commerce style product pages from structured data"""
    
    def __init__(self):
        self.template = self._create_template()
    
    def generate(self, structured_data: Dict[str, Any], output_path: str = "product_catalog.html") -> str:
        """Generate HTML from structured product data"""
        print(f"\n=== Generating HTML ===")
        
        # Render the template
        html = self.template.render(
            product_family=structured_data.get('product_family', 'Product Catalog'),
            category=structured_data.get('category', 'Products'),
            products=structured_data.get('products', [])
        )
        
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"HTML generated: {output_path}")
        return html
    
    def _create_template(self) -> Template:
        """Create Jinja2 template for product page"""
        
        template_str = """<!DOCTYPE html>
<html lang="{{ language }}"{% if is_rtl %} dir="rtl"{% endif %}>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ product_family }} - Product Catalog</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: {% if language == 'fa' %}'Vazirmatn', 'Tahoma', 'Arial'{% elif language == 'zh' %}'Microsoft YaHei', 'SimHei', 'Arial'{% else %}-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif{% endif %};
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
            direction: {% if is_rtl %}rtl{% else %}ltr{% endif %};
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .header .category {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .product-card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }
        
        .product-header {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 2rem;
        }
        
        .product-header h2 {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        .product-header .model {
            font-size: 1.2rem;
            opacity: 0.9;
            font-weight: 500;
        }
        
        .product-header .tagline {
            margin-top: 1rem;
            font-size: 1.1rem;
            font-style: italic;
            opacity: 0.95;
        }
        
        .product-body {
            padding: 2rem;
        }
        
        .section {
            margin-bottom: 2rem;
        }
        
        .section-title {
            font-size: 1.5rem;
            color: #667eea;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #667eea;
        }
        
        .description {
            font-size: 1.1rem;
            line-height: 1.8;
            color: #555;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
        }
        
        .feature-item {
            background: #f8f9ff;
            padding: 1rem;
            border-radius: 8px;
            {% if is_rtl %}border-right{% else %}border-left{% endif %}: 4px solid #667eea;
            display: flex;
            align-items: start;
        }
        
        .feature-item::before {
            content: "✓";
            color: #667eea;
            font-weight: bold;
            font-size: 1.2rem;
            {% if is_rtl %}margin-left{% else %}margin-right{% endif %}: 0.8rem;
        }
        
        .specs-table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }
        
        .specs-category {
            background: #667eea;
            color: white;
            padding: 0.8rem;
            font-weight: 600;
            font-size: 1.1rem;
        }
        
        .specs-table tr {
            border-bottom: 1px solid #e0e0e0;
        }
        
        .specs-table td {
            padding: 0.8rem;
        }
        
        .specs-table td:first-child {
            font-weight: 600;
            color: #555;
            width: 40%;
            background: #f8f9ff;
        }
        
        .specs-table td:last-child {
            color: #333;
        }
        
        .applications {
            display: flex;
            flex-wrap: wrap;
            gap: 0.8rem;
        }
        
        .application-tag {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.6rem 1.2rem;
            border-radius: 20px;
            font-weight: 500;
        }
        
        .pricing-box {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            margin-top: 2rem;
        }
        
        .pricing-box .price {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .pricing-box .price-label {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .add-to-cart-btn {
            background: #f5576c;
            color: white;
            border: none;
            padding: 1rem 3rem;
            font-size: 1.2rem;
            font-weight: 600;
            border-radius: 50px;
            cursor: pointer;
            margin-top: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
        }
        
        .add-to-cart-btn:hover {
            background: #e04456;
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(245, 87, 108, 0.6);
        }
        
        .images-section {
            background: #f8f9ff;
            padding: 1.5rem;
            border-radius: 8px;
        }
        
        .image-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        
        .image-tag {
            background: white;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            border: 2px solid #667eea;
            color: #667eea;
            font-weight: 500;
        }
        
        .rating {
            display: flex;
            align-items: center;
            margin: 1rem 0;
        }
        
        .stars {
            color: #ffa500;
            font-size: 1.5rem;
            margin-right: 0.5rem;
        }
        
        .rating-text {
            color: #666;
            font-size: 1rem;
        }
        
        .badge {
            display: inline-block;
            background: #11998e;
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.9rem;
            font-weight: 600;
            margin-left: 1rem;
        }
        
        .product-grid {
            display: grid;
            gap: 2rem;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 1.8rem;
            }
            
            .product-header h2 {
                font-size: 1.5rem;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
            }
            
            .pricing-box .price {
                font-size: 2rem;
            }
        }
        
        .footer {
            background: #333;
            color: white;
            padding: 2rem;
            text-align: center;
            margin-top: 3rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>{{ product_family }}</h1>
            <div class="category">{{ category }}</div>
        </div>
    </div>
    
    <div class="container">
        <div class="product-grid">
            {% for product in products %}
            <div class="product-card">
                <div class="product-header">
                    <h2>{{ product.name }}</h2>
                    <div class="model">Model: {{ product.model }}</div>
                    {% if product.tagline %}
                    <div class="tagline">{{ product.tagline }}</div>
                    {% endif %}
                </div>
                
                <div class="product-body">
                    <div class="rating">
                        <div class="stars">★★★★★</div>
                        <div class="rating-text">(4.8 out of 5)</div>
                        <span class="badge">Premium Quality</span>
                    </div>
                    
                    {% if product.description %}
                    <div class="section">
                        <h3 class="section-title">Product Description</h3>
                        <p class="description">{{ product.description }}</p>
                    </div>
                    {% endif %}
                    
                    {% if product.features %}
                    <div class="section">
                        <h3 class="section-title">Key Features</h3>
                        <div class="features-grid">
                            {% for feature in product.features %}
                            <div class="feature-item">{{ feature }}</div>
                            {% endfor %}
                        </div>
                    </div>
                    {% endif %}
                    
                    {% if product.specifications %}
                    <div class="section">
                        <h3 class="section-title">Technical Specifications</h3>
                        <table class="specs-table">
                            {% for category, specs in product.specifications.items() %}
                                {% if specs is mapping %}
                                <tr>
                                    <td colspan="2" class="specs-category">{{ category }}</td>
                                </tr>
                                {% for spec_name, spec_value in specs.items() %}
                                <tr>
                                    <td>{{ spec_name }}</td>
                                    <td>{{ spec_value }}</td>
                                </tr>
                                {% endfor %}
                                {% else %}
                                <tr>
                                    <td>{{ category }}</td>
                                    <td>{{ specs }}</td>
                                </tr>
                                {% endif %}
                            {% endfor %}
                        </table>
                    </div>
                    {% endif %}
                    
                    {% if product.applications %}
                    <div class="section">
                        <h3 class="section-title">Applications</h3>
                        <div class="applications">
                            {% for app in product.applications %}
                            <div class="application-tag">{{ app }}</div>
                            {% endfor %}
                        </div>
                    </div>
                    {% endif %}
                    
                    {% if product.images %}
                    <div class="section">
                        <h3 class="section-title">Product Images</h3>
                        <div class="images-section">
                            <div class="image-tags">
                                {% for image in product.images %}
                                <div class="image-tag">📷 {{ image }}</div>
                                {% endfor %}
                            </div>
                        </div>
                    </div>
                    {% endif %}
                    
                    <div class="pricing-box">
                        <div class="price-label">Price</div>
                        <div class="price">{{ product.pricing.price }}</div>
                        <button class="add-to-cart-btn" onclick="alert('Added to cart!')">Add to Cart</button>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <div class="footer">
        <p>Generated by PDF to Shopping Card Converter</p>
        <p>© 2025 - All Rights Reserved</p>
    </div>
    
    <script>
        // Add interactive features
        document.querySelectorAll('.product-card').forEach(card => {
            card.addEventListener('click', function(e) {
                if (!e.target.classList.contains('add-to-cart-btn')) {
                    this.style.backgroundColor = '#f8f9ff';
                    setTimeout(() => {
                        this.style.backgroundColor = 'white';
                    }, 200);
                }
            });
        });
        
        // Add to cart functionality
        let cartCount = 0;
        document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.stopPropagation();
                cartCount++;
                this.textContent = '✓ Added to Cart';
                this.style.background = '#11998e';
                
                setTimeout(() => {
                    this.textContent = 'Add to Cart';
                    this.style.background = '#f5576c';
                }, 2000);
            });
        });
    </script>
</body>
</html>
"""
        
        return Template(template_str)

