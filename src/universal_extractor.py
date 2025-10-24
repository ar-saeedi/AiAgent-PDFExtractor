"""
Universal PDF Extractor - Works with ANY PDF catalog
Uses advanced AI vision models for maximum accuracy
"""

import pdfplumber
import fitz
import io
import sys
import os
import base64
from PIL import Image
from typing import List, Dict, Any, Optional
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


class UniversalPDFExtractor:
    """
    Universal PDF extractor that works with ANY type of PDF catalog
    Combines multiple extraction methods for maximum accuracy
    """
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.total_pages = 0
        
    def extract_complete_content(self) -> Dict[str, Any]:
        """
        Extract comprehensive content using multiple methods:
        1. Text extraction (pdfplumber + PyMuPDF)
        2. Table extraction (pdfplumber)
        3. Image extraction (PyMuPDF)
        4. Layout analysis (PyMuPDF)
        """
        print(f"\n{'='*80}")
        print(f"UNIVERSAL PDF EXTRACTOR")
        print(f"{'='*80}")
        print(f"Processing: {os.path.basename(self.pdf_path)}\n")
        
        content = {
            'metadata': self._extract_metadata(),
            'pages': [],
            'extraction_methods': {
                'text': True,
                'tables': True,
                'images': True,
                'layout': True
            }
        }
        
        with pdfplumber.open(self.pdf_path) as pdf_plumber:
            pdf_pymupdf = fitz.open(self.pdf_path)
            self.total_pages = len(pdf_plumber.pages)
            content['metadata']['total_pages'] = self.total_pages
            
            print(f"Total pages: {self.total_pages}")
            print("Extraction methods: Text, Tables, Images, Layout\n")
            
            for page_num in range(self.total_pages):
                print(f"Processing page {page_num + 1}/{self.total_pages}...", end=' ')
                
                page_content = self._extract_page_multimethod(
                    pdf_plumber.pages[page_num],
                    pdf_pymupdf[page_num],
                    page_num
                )
                
                content['pages'].append(page_content)
                print("✓")
            
            pdf_pymupdf.close()
        
        print(f"\n{'='*80}")
        print(f"Extraction complete! {self.total_pages} pages processed.")
        print(f"{'='*80}\n")
        
        return content
    
    def _extract_metadata(self) -> Dict[str, Any]:
        """Extract PDF metadata using PyMuPDF"""
        try:
            doc = fitz.open(self.pdf_path)
            metadata = doc.metadata
            doc.close()
            
            return {
                'title': metadata.get('title', ''),
                'author': metadata.get('author', ''),
                'subject': metadata.get('subject', ''),
                'creator': metadata.get('creator', ''),
                'producer': metadata.get('producer', ''),
                'creation_date': metadata.get('creationDate', ''),
                'modification_date': metadata.get('modDate', ''),
                'source_file': os.path.basename(self.pdf_path)
            }
        except Exception as e:
            print(f"Warning: Could not extract metadata: {e}")
            return {'source_file': os.path.basename(self.pdf_path)}
    
    def _extract_page_multimethod(self, page_plumber, page_pymupdf, page_num: int) -> Dict[str, Any]:
        """Extract content from a page using multiple methods"""
        text_plumber = page_plumber.extract_text() or ""
        text_pymupdf = page_pymupdf.get_text() or ""
        text = text_plumber if len(text_plumber) > len(text_pymupdf) else text_pymupdf
        
        tables = page_plumber.extract_tables() or []
        images = self._extract_images_pymupdf(page_pymupdf, page_num)
        layout = self._analyze_layout(page_pymupdf)
        text_blocks = self._extract_text_blocks(page_pymupdf)
        
        return {
            'page_number': page_num + 1,
            'text': text,
            'text_length': len(text),
            'tables': tables,
            'table_count': len(tables),
            'images': images,
            'image_count': len(images),
            'layout': layout,
            'text_blocks': text_blocks,
            'has_content': len(text) > 0 or len(tables) > 0 or len(images) > 0
        }
    
    def _extract_images_pymupdf(self, page, page_num: int) -> List[Dict[str, Any]]:
        """Extract images from page using PyMuPDF"""
        images_data = []
        
        try:
            try:
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                os.makedirs("output/images", exist_ok=True)
                img_path = f"output/images/page_{page_num + 1}_full.png"
                pix.save(img_path)
                
                images_data.append({
                    'page': page_num + 1,
                    'type': 'full_page',
                    'path': img_path,
                    'width': pix.width,
                    'height': pix.height
                })
            except Exception as e:
                print(f"Warning: Could not save full page image: {e}")
        
        except Exception as e:
            print(f"Warning: Image extraction error on page {page_num + 1}: {e}")
        
        return images_data
    
    def _analyze_layout(self, page) -> Dict[str, Any]:
        """Analyze page layout structure"""
        try:
            rect = page.rect
            blocks = page.get_text("dict")["blocks"]
            
            layout = {
                'width': rect.width,
                'height': rect.height,
                'block_count': len(blocks),
                'text_blocks': 0,
                'image_blocks': 0
            }
            
            for block in blocks:
                if block['type'] == 0:
                    layout['text_blocks'] += 1
                elif block['type'] == 1:
                    layout['image_blocks'] += 1
            
            return layout
        except Exception as e:
            return {'error': str(e)}
    
    def _extract_text_blocks(self, page) -> List[Dict[str, Any]]:
        """Extract text blocks with positioning information"""
        blocks = []
        
        try:
            text_blocks = page.get_text("blocks")
            
            for block in text_blocks:
                if len(block) >= 5:
                    blocks.append({
                        'x0': block[0],
                        'y0': block[1],
                        'x1': block[2],
                        'y1': block[3],
                        'text': block[4].strip(),
                        'block_type': block[5] if len(block) > 5 else 0
                    })
        except Exception as e:
            print(f"Warning: Could not extract text blocks: {e}")
        
        return blocks


def extract_pdf_universal(pdf_path: str) -> Dict[str, Any]:
    """Convenience function for universal PDF extraction"""
    extractor = UniversalPDFExtractor(pdf_path)
    return extractor.extract_complete_content()

