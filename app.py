import gradio as gr
from src.query import ask


def handle_query(question):
    result = ask(question)

    sources = "\n".join(f"- {source}" for source in result["sources"])

    return result["answer"], sources


with gr.Blocks() as demo:
    gr.Markdown("# The Unofficial Guide")
    gr.Markdown("Ask questions about SJSU Computer Science professor reviews.")

    question = gr.Textbox(label="Your question", placeholder="Which professor does not respond to emails?")
    ask_button = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved sources", lines=5)

    ask_button.click(handle_query, inputs=question, outputs=[answer, sources])
    question.submit(handle_query, inputs=question, outputs=[answer, sources])

demo.launch()