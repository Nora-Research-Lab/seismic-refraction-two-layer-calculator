import gradio as gr
import matplotlib
matplotlib.use('Agg')
from seismic_refraction_two_layer_calculator import (
    parse_distances_and_times,
    compute_two_layer,
    generate_plot,
    generate_csv
)

def compute_and_plot(dist_str, time_str):
    try:
        distances, times = parse_distances_and_times(dist_str, time_str)
    except (ValueError, TypeError) as e:
        return "Invalid input: " + str(e), None, None

    try:
        result = compute_two_layer(distances, times)
    except (ValueError, RuntimeError) as e:
        return "Calculation error: " + str(e), None, None

    fig = generate_plot(
        distances, times,
        result['direct_times_fitted'],
        result['refracted_times_fitted'],
        result['v1'], result['v2'],
        result['crossover_distance']
    )

    text = f"""V1 = {result['v1']:.2f} km/s
V2 = {result['v2']:.2f} km/s
Depth to interface = {result['depth']:.2f} m
Crossover distance = {result['crossover_distance']:.2f} m
Intercept time = {result['intercept_time']:.2f} ms
Classification: {result['classification']}"""

    csv_content = generate_csv(distances, times,
                               result['direct_times_fitted'],
                               result['refracted_times_fitted'])

    return text, fig, csv_content

with gr.Blocks(title="Seismic Refraction Two-Layer Calculator") as demo:
    gr.Markdown("# Seismic Refraction Two-Layer Calculator (Intercept-Time Method)")

    with gr.Row():
        with gr.Column(scale=1):
            dist_input = gr.Textbox(
                label="Distances (m, comma-separated)",
                placeholder="e.g., 0,10,20,30,40,50,60,70,80,90,100"
            )
            time_input = gr.Textbox(
                label="First arrival times (ms, comma-separated)",
                placeholder="e.g., 0.0,10.2,20.5,25.8,30.1,34.0,37.5,40.8,43.9,46.8,49.5"
            )
            compute_btn = gr.Button("Compute")

        with gr.Column(scale=1):
            output_text = gr.Textbox(label="Results")
            output_plot = gr.Plot(label="Travel-Time Graph")

    with gr.Row():
        csv_output = gr.Textbox(label="CSV content (copy or download below)", visible=False)
        download_btn = gr.DownloadButton("Download CSV", variant="secondary")

    def process_and_return(dist_str, time_str):
        text, fig, csv_content = compute_and_plot(dist_str, time_str)
        return text, fig, csv_content

    compute_btn.click(
        fn=process_and_return,
        inputs=[dist_input, time_input],
        outputs=[output_text, output_plot, csv_output]
    )

    download_btn.click(
        fn=lambda csv_content: csv_content,
        inputs=[csv_output],
        outputs=download_btn
    )

    gr.Examples(
        examples=[
            ["0,10,20,30,40,50,60,70,80,90,100",
             "0.0,10.2,20.5,25.8,30.1,34.0,37.5,40.8,43.9,46.8,49.5"],
        ],
        inputs=[dist_input, time_input]
    )

demo.launch(server_name="0.0.0.0", server_port=7860)
