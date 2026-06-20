import difflib
import gradio as gr
from utils import compute_diff, rewrite_text

# --- Frontend UI Definition ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# AI Text Sculptor")
    gr.Markdown("Adjust the dials to instantly rewrite any text. The system will highlight exactly what was added or removed.")
    
    with gr.Row():
        # Left Column: Inputs & Controls
        with gr.Column(scale=1):
            source_text = gr.Textbox(label="Original Text", lines=8, placeholder="Paste your draft here...")
            
            with gr.Row():
                tone_dropdown = gr.Dropdown(
                    choices=["Formal", "Casual", "Persuasive", "Empathetic", "Direct"], 
                    value="Formal", 
                    label="Tone"
                )
                length_radio = gr.Radio(
                    choices=["Shorter", "Similar Length", "Longer & Detailed"], 
                    value="Similar Length", 
                    label="Length"
                )
                
            with gr.Row():
                audience_dropdown = gr.Dropdown(
                    choices=["General Public", "Domain Experts", "C-Suite Executives", "Children"], 
                    value="General Public", 
                    label="Target Audience"
                )
                style_dropdown = gr.Dropdown(
                    choices=["Modern & Clean", "Academic", "Journalistic", "Creative Storytelling"], 
                    value="Modern & Clean", 
                    label="Language Style"
                )
                
            submit_btn = gr.Button("Rewrite Text", variant="primary")
            
        # Right Column: Outputs
        with gr.Column(scale=1):
            final_output = gr.Textbox(label="Rewritten Result", lines=8)
            
            gr.Markdown("### Before/After Analysis")
            diff_view = gr.HighlightedText(
                label="Text Differences",
                color_map={"+": "green", "-": "red"},
                show_legend=True
            )
            
    # Connect the UI to the Python backend
    submit_btn.click(
        fn=rewrite_text,
        inputs=[source_text, tone_dropdown, length_radio, audience_dropdown, style_dropdown],
        outputs=[final_output, diff_view]
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)