import os
import jinja2
import pdfkit
import pandas as pd
import numpy as np
from datetime import date
import json
from types import SimpleNamespace

def render_html(company_data, risk_data, climate_data):
    """
    Render html page using jinja based on layout.html
    """
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "layout.html"
    template = template_env.get_template(template_file)
    output_text = template.render(
        company_name=company_data.Name,
        date=get_date(),
        risks=risk_data.risks,
        mitigations=risk_data.mitigations
        )

    html_path = f'./res/{company_data.Name}_sustainability_report.html'
    html_file = open(html_path, 'w')
    html_file.write(output_text)
    html_file.close()
    print(f"Now converting {company_data.Name} ... ")
    pdf_path = f'./res/{company_data.Name}_sustainability_report.pdf'    
    html2pdf(html_path, pdf_path)   

def html2pdf(html_path, pdf_path):
    """
    Convert html to pdf using pdfkit which is a wrapper of wkhtmltopdf
    """
    options = {
        'page-size': 'Letter',
        'margin-top': '0.35in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None
    }
    with open(html_path) as f:
        pdfkit.from_file(f, pdf_path, options=options)

def get_date():
    "Get today's date in German format"
    today = date.today()
    return today.strftime("%d.%m.%Y")

if __name__ == "__main__":

    # df = pd.read_csv('tables/sample.csv')
    # for row in df.itertuples():
    company_data = json.loads('{"Name": "Company A"}', object_hook=lambda d: SimpleNamespace(**d))
    risk_data = json.loads('{"risks": ["Risk 1", "Risk 2", "Risk 3"], "mitigations": ["Mitigation 1", "Mitigation 2", "Mitigation 3"]}', object_hook=lambda d: SimpleNamespace(**d))
    climate_data = {
    }
    render_html(company_data=company_data, risk_data=risk_data, climate_data=climate_data)