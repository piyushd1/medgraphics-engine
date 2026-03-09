from engine.pipeline import clean_markdown_block

def test_clean_markdown_block_empty():
    assert clean_markdown_block("") == ""
