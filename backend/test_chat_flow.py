import os
import shutil
from unittest.mock import patch, MagicMock

os.environ["GEMINI_API_KEY"] = "sk-dummy"

from rag import rag_service

# Patch where it is imported in rag.py? 
# In rag.py `answer_question`, we do `import google.generativeai as genai`
# So we must patch `google.generativeai` in sys.modules or patch the module if it was top level.
# Since it is a local import, we can patch `google.generativeai` globally before the function runs.

@patch("google.generativeai.GenerativeModel")
@patch("google.generativeai.configure")
@patch("rag.retrieve_chunks")
def test_chat_flow(mock_retrieve, mock_configure, mock_model_cls):
    print("Testing Gemini chat flow...")
    
    # Mock Retrieval: Return some context
    mock_retrieve.return_value = ["Deductible is $500.", "File claims online."]
    
    # Mock Gemini Generation
    mock_model_instance = mock_model_cls.return_value
    mock_model_instance.generate_content.return_value = MagicMock(text="The deductible is $500.")
    
    # Run Chat
    answer = rag_service.answer_question("What is the deductible?")
    print("Answer:", answer)
    
    assert "The deductible is $500." in answer
    print("Chat successful.")
    
    # Verify retrieval called
    mock_retrieve.assert_called()
    # Verify configure called
    mock_configure.assert_called()

if __name__ == "__main__":
    test_chat_flow()
