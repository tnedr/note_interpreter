from note_interpreter.io import InputHandler, OutputGenerator

if __name__ == "__main__":
    batch = InputHandler.load_batch(
        "docs/examples/example_notes.csv",
        "docs/examples/example_user_memory.md",
        "docs/examples/example_classification.yaml"
    )
    OutputGenerator.write_notes_csv(batch.notes, "output_notes.csv")
    print("Pipeline run complete. Output written to output_notes.csv") 