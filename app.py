import gradio as gr
from rewriter_core import TextRewriter

# Initialize the backend engine
engine = TextRewriter()

def route_rewrite(text, tone, length, audience, style):
    """Wrapper function to connect Gradio inputs to the backend engine."""
    return engine.process_text(text, tone, length, audience, style)

# Build the UI
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# AI Text Sculptor")
    
    with gr.Row():
        with gr.Column(scale=1):
            source_text = gr.Textbox(label="Original Text", lines=8)
            tone_dropdown = gr.Dropdown(choices=["Formal", "Casual", "Persuasive"], value="Formal", label="Tone")
            length_radio = gr.Radio(choices=["Shorter", "Similar Length", "Longer"], value="Similar Length", label="Length")
            audience_dropdown = gr.Dropdown(choices=["General Public", "Domain Experts"], value="General Public", label="Target Audience")
            style_dropdown = gr.Dropdown(choices=["Modern", "Academic", "Journalistic"], value="Modern", label="Style")
            submit_btn = gr.Button("Rewrite Text", variant="primary")
            
        with gr.Column(scale=1):
            final_output = gr.Textbox(label="Rewritten Result", lines=8)
            diff_view = gr.HighlightedText(label="Text Differences", color_map={"+": "green", "-": "red"})
            
    # Connect the UI to the wrapper function
    submit_btn.click(
        fn=route_rewrite,
        inputs=[source_text, tone_dropdown, length_radio, audience_dropdown, style_dropdown],
        outputs=[final_output, diff_view]
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
