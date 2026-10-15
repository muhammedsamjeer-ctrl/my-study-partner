from io import BytesIO

import streamlit as st
import ollama
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

st.title("🤖 HI TELL ME SOMETHING")
st.caption("CREATED BY SAMJEER")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "doc_title" not in st.session_state:
    st.session_state.doc_title = "Monthly Business Summary"

if "doc_content" not in st.session_state:
    st.session_state.doc_content = """# Monthly Business Summary

## Overview
- Revenue: ₹1,25,000
- Expenses: ₹68,000
- Net Profit: ₹57,000

## Notes
This document was created using the AI assistant document builder.
"""

if "doc_type" not in st.session_state:
    st.session_state.doc_type = "Business Summary"

if "analysis_document" not in st.session_state:
    st.session_state.analysis_document = """# Sample Business Report

Company: Samjeer Tech Solutions

Revenue: ₹1,25,000
Expenses: ₹68,000
Net Profit: ₹57,000

This report shows healthy performance and good growth opportunities in the next quarter.
"""

if "analysis_prompt" not in st.session_state:
    st.session_state.analysis_prompt = (
        "Analyze this document, identify the main business insights, "
        "and recreate it in a cleaner professional format for a client report."
    )

if "invoice_data" not in st.session_state:
    st.session_state.invoice_data = {
        "customer": "Samjeer Business Solutions",
        "invoice_no": "INV-2026-001",
        "date": "15 Oct 2026",
        "items": [
            {"name": "Website Design", "qty": 1, "price": 25000},
            {"name": "SEO Package", "qty": 1, "price": 18000},
            {"name": "Hosting", "qty": 3, "price": 2000}
        ],
        "gst": 18
    }

with st.sidebar:
    st.header("Workspace")
    selected_tab = st.radio(
        "Choose a section",
        [
            "Chat",
            "Document Creation",
            "Document Analysis & Recreate",
            "Invoice Generator",
            "Business Report",
            "Accounting Presentation"
        ],
        index=0
    )


def create_pdf_from_text(text, title="Document"):
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    styles = getSampleStyleSheet()
    story = [Paragraph(title, styles["Title"]), Spacer(1, 12)]

    for line in text.splitlines():
        clean_line = line.strip()
        if not clean_line:
            story.append(Spacer(1, 8))
            continue

        if clean_line.startswith("# "):
            story.append(Paragraph(clean_line[2:], styles["Heading1"]))
        elif clean_line.startswith("## "):
            story.append(Paragraph(clean_line[3:], styles["Heading2"]))
        elif clean_line.startswith("### "):
            story.append(Paragraph(clean_line[4:], styles["Heading3"]))
        else:
            story.append(Paragraph(clean_line.replace("**", ""), styles["BodyText"]))

    document.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data


def write_document(doc_type_value, doc_title_value, doc_content_value):
    document_text = f"# {doc_title_value}\n\n**Type:** {doc_type_value}\n\n{doc_content_value}\n"
    st.session_state.doc_title = doc_title_value
    st.session_state.doc_content = doc_content_value
    st.session_state.doc_type = doc_type_value
    st.success("Document created successfully.")
    st.download_button(
        label="Download Markdown File",
        data=document_text,
        file_name=f"{doc_title_value.lower().replace(' ', '_')}.md",
        mime="text/markdown"
    )
    st.download_button(
        label="Download PDF",
        data=create_pdf_from_text(document_text, doc_title_value),
        file_name=f"{doc_title_value.lower().replace(' ', '_')}.pdf",
        mime="application/pdf"
    )
    st.markdown("### Preview")
    st.markdown(document_text)


if selected_tab == "Chat":
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask me anything in Malayalam or English...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI is thinking..."):
                try:
                    response = ollama.chat(
                        model="llama3.2:3b",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are a helpful personal AI assistant. "
                                    "Reply in Malayalam when the user speaks "
                                    "Malayalam. Otherwise, follow the user's "
                                    "language. Be clear and accurate."
                                )
                            },
                            *st.session_state.messages
                        ]
                    )

                    answer = response["message"]["content"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})

                except Exception as error:
                    st.error(
                        "AI connection failed. "
                        "Check whether Ollama is running "
                        "and the model is installed."
                    )
                    st.caption(str(error))

elif selected_tab == "Document Creation":
    st.header("📄 Document Creation")

    with st.form("document_form"):
        doc_type = st.selectbox(
            "Document Type",
            [
                "Business Summary",
                "Financial Report",
                "Proposal",
                "Meeting Notes",
                "Client Letter",
                "Invoice",
                "GST Report",
                "Malayalam Business Letter",
                "Malayalam Invoice",
            ],
        )

        document_templates = {
            "Business Summary": "# Monthly Business Summary\n\n## Overview\n- Revenue: ₹1,25,000\n- Expenses: ₹68,000\n- Net Profit: ₹57,000\n\n## Notes\nThis summary is prepared for business review.",
            "Financial Report": "# Financial Report\n\n## Executive Summary\nRevenue increased by 12% compared to the previous month. Operating costs remain stable.\n\n## Balance Sheet\n- Cash: ₹55,000\n- Inventory: ₹35,000\n- Liabilities: ₹20,000\n- Equity: ₹70,000",
            "Proposal": "# Business Proposal\n\n## Objective\nTo improve operational efficiency and customer reach through a digital transformation project.\n\n## Scope\n1. Website modernization\n2. CRM setup\n3. Automated reporting",
            "Meeting Notes": "# Meeting Notes\n\n## Agenda\n- Team performance review\n- Budget planning\n- Marketing campaign update\n\n## Action Items\n- Finalize budget approval\n- Share sales report\n- Prepare campaign schedule",
            "Client Letter": "# Client Letter\n\nDear Client,\n\nThank you for your continued trust in our services. We are pleased to share the latest business updates and confirm our commitment to your success.",
            "Invoice": "# Invoice\n\n**Invoice Number:** INV-2026-001\n**Date:** 15 Oct 2026\n\n| Item | Qty | Amount |\n|---|---:|---:|\n| Web Design | 1 | ₹25,000 |\n| SEO Package | 1 | ₹18,000 |\n| Hosting | 3 | ₹2,000 |\n\n**Total:** ₹45,000",
            "GST Report": "# GST Report\n\n## GST Details\n- CGST: ₹8,500\n- SGST: ₹8,500\n- Total GST: ₹17,000\n\n## Tax Summary\nThe business is compliant with current GST reporting requirements.",
            "Malayalam Business Letter": "# ഫംപാനി അല്ലെങ്കിൽ ബിസിനസ്സ് ലെറ്റർ\n\nവിശ്വസ്തരായ ക്ലെയന്റുമാർക്ക്,\n\nനിങ്ങളുടെ കരാറിന് അനുസരിച്ച് ഞങ്ങളുടെ സേവനങ്ങൾ തുടർന്നുകൊണ്ടിരിക്കുന്നു. നിങ്ങളുടെ ബിസിനസിന് പ്രാധാന്യമായ സജീവമായ പിന്തുണയും സഹായവും നല്കുന്നതിന് ഞങ്ങൾ തയാറാണ്.",
            "Malayalam Invoice": "# വേണന്തം ഇന്വോയ്സ്\n\n**ഇൻവോയ്സ് നമ്പർ:** INV-ML-001\n**തീയതി:** 15 ഒക്ടോബ് 2026\n\n| ഇനം | അളവ് | തുക |\n|---|---:|---:|\n| വെബ്സൈറ്റ് രൂപകൽപ്പന | 1 | ₹25,000 |\n|എസ്‌ഇഒ പാക്കേജ് | 1 | ₹18,000 |\n\n**മൊത്തം:** ₹43,000",
        }

        doc_title = st.text_input("Document Title", value=st.session_state.doc_title)
        template_choice = st.checkbox("Use suggested template", value=True)

        template_content = document_templates.get(doc_type, st.session_state.doc_content)
        default_content = template_content if template_choice else st.session_state.doc_content
        doc_content = st.text_area(
            "Document Content",
            value=default_content,
            height=240,
        )

        submitted = st.form_submit_button("Generate Document")

    if submitted:
        write_document(doc_type, doc_title, doc_content)

elif selected_tab == "Document Analysis & Recreate":
    st.header("🧠 Document Analysis & Recreate")
    st.caption("Paste an existing document and ask the AI to rewrite it in the format you want.")

    with st.form("analysis_recreate_form"):
        source_document = st.text_area(
            "Original Document",
            value=st.session_state.analysis_document,
            height=220,
        )
        recreate_prompt = st.text_area(
            "What should the recreated document look like?",
            value=st.session_state.analysis_prompt,
            height=120,
        )
        analyze_submit = st.form_submit_button("Analyze & Recreate")

    if analyze_submit:
        st.session_state.analysis_document = source_document
        st.session_state.analysis_prompt = recreate_prompt

        with st.spinner("Analyzing document and recreating it based on your request..."):
            try:
                response = ollama.chat(
                    model="llama3.2:3b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a professional business document analyst and editor. "
                                "Read the original document carefully, explain the key meaning and structure, "
                                "then rewrite it into a polished, professional version based on the user's prompt. "
                                "Return the result in clear sections: 'Analysis', 'Recreated Document'. "
                                "Use the user's preferred language when possible."
                            )
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Original Document:\n{source_document}\n\n"
                                f"User Prompt:\n{recreate_prompt}"
                            )
                        }
                    ]
                )

                result = response["message"]["content"]
                st.markdown(result)
        
                st.download_button(
                    label="Download Recreated Markdown",
                    data=result,
                    file_name="recreated_document.md",
                    mime="text/markdown"
                )
                st.download_button(
                    label="Download Recreated PDF",
                    data=create_pdf_from_text(result, "Recreated Document"),
                    file_name="recreated_document.pdf",
                    mime="application/pdf"
                )

            except Exception as error:
                st.error("Document analysis failed. Please check Ollama and the model connection.")
                st.caption(str(error))

elif selected_tab == "Invoice Generator":
    st.header("🧾 Invoice Generator")

    st.subheader("Customer & Invoice Details")
    with st.form("invoice_form"):
        customer = st.text_input("Customer Name", value=st.session_state.invoice_data["customer"])
        invoice_no = st.text_input("Invoice Number", value=st.session_state.invoice_data["invoice_no"])
        invoice_date = st.text_input("Invoice Date", value=st.session_state.invoice_data["date"])
        gst_rate = st.number_input("GST Rate (%)", min_value=0, max_value=30, value=18)

        item_name = st.text_input("Item Name", value="Website Design")
        item_qty = st.number_input("Quantity", min_value=1, value=1)
        item_price = st.number_input("Unit Price (₹)", min_value=0, value=25000)

        add_item = st.form_submit_button("Add Item")

    if add_item:
        st.session_state.invoice_data["customer"] = customer
        st.session_state.invoice_data["invoice_no"] = invoice_no
        st.session_state.invoice_data["date"] = invoice_date
        st.session_state.invoice_data["gst"] = gst_rate
        st.session_state.invoice_data["items"].append(
            {"name": item_name, "qty": int(item_qty), "price": float(item_price)}
        )

    items = st.session_state.invoice_data["items"]
    subtotal = sum(item["qty"] * item["price"] for item in items)
    gst_value = subtotal * (st.session_state.invoice_data["gst"] / 100)
    total = subtotal + gst_value

    st.subheader("Preview")
    st.markdown(f"## Invoice: {invoice_no}")
    st.markdown(f"**Customer:** {customer}")
    st.markdown(f"**Date:** {invoice_date}")

    invoice_table = {
        "Item": [item["name"] for item in items],
        "Qty": [item["qty"] for item in items],
        "Unit Price": [f"₹{item['price']:,.0f}" for item in items],
        "Amount": [f"₹{item['qty'] * item['price']:,.0f}" for item in items],
    }
    st.table(invoice_table)

    col1, col2, col3 = st.columns(3)
    col1.metric("Subtotal", f"₹{subtotal:,.0f}")
    col2.metric("GST", f"₹{gst_value:,.0f}")
    col3.metric("Total", f"₹{total:,.0f}")

    invoice_markdown = f"# {invoice_no}\n\n**Customer:** {customer}\n**Date:** {invoice_date}\n\n| Item | Qty | Amount |\n|---|---:|---:|\n"
    for item in items:
        invoice_markdown += f"| {item['name']} | {item['qty']} | ₹{item['qty'] * item['price']:,.0f} |\n"
    invoice_markdown += f"\n**Subtotal:** ₹{subtotal:,.0f}\n**GST:** ₹{gst_value:,.0f}\n**Total:** ₹{total:,.0f}\n"

    st.download_button(
        label="Download Invoice Markdown",
        data=invoice_markdown,
        file_name=f"{invoice_no}.md",
        mime="text/markdown"
    )
    st.download_button(
        label="Download Invoice PDF",
        data=create_pdf_from_text(invoice_markdown, f"Invoice {invoice_no}"),
        file_name=f"{invoice_no}.pdf",
        mime="application/pdf"
    )

elif selected_tab == "Business Report":
    st.header("📊 Business Report")
    st.subheader("Quarterly Business Performance")

    revenue = [250000, 280000, 320000, 360000]
    expenses = [180000, 195000, 210000, 225000]
    profit = [value - expense for value, expense in zip(revenue, expenses)]

    summary_data = {
        "Quarter": ["Q1", "Q2", "Q3", "Q4"],
        "Revenue": revenue,
        "Expenses": expenses,
        "Profit": profit,
    }
    st.line_chart(summary_data, x="Quarter")
    st.table(summary_data)

    col1, col2, col3 = st.columns(3)
    col1.metric("Annual Revenue", f"₹{sum(revenue):,.0f}")
    col2.metric("Annual Expenses", f"₹{sum(expenses):,.0f}")
    col3.metric("Annual Profit", f"₹{sum(profit):,.0f}")

    st.markdown(
        """
        ### Business Notes
        - Sales performance is improving steadily.
        - Operating costs are controlled with moderate growth.
        - Profit margin remains healthy and sustainable.
        """
    )

else:
    st.header("💰 GST / Accounting Dashboard")

    revenue = 125000
    expenses = 68000
    profit = revenue - expenses
    gst_amount = revenue * 0.18
    cash_flow = [12000, 18500, 21000, 17500, 24500, 26000, 28000]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Revenue", "₹1,25,000")
    col2.metric("Expenses", "₹68,000")
    col3.metric("Net Profit", "₹57,000")
    col4.metric("GST", "₹22,500")

    st.subheader("Monthly Cash Flow")
    st.bar_chart({"Cash Flow": cash_flow})

    st.subheader("GST & Expense Breakdown")
    gst_data = {
        "Category": ["Taxable Sales", "GST Collected", "Input Tax", "Net GST Payable"],
        "Amount": [125000, 22500, 6000, 16500],
    }
    st.bar_chart(gst_data, x="Category", y="Amount")

    st.subheader("Summary Table")
    st.table(
        {
            "Category": ["Income", "Expenses", "GST", "Profit"],
            "Amount": [revenue, expenses, gst_amount, profit],
            "Currency": ["INR", "INR", "INR", "INR"],
        }
    )

    st.caption("This GST and accounting dashboard is designed for quick business financial review and tax overview.")

