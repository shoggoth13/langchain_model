from typing import Optional, TypeVar, Any, Callable, Type

from langchain.chains.openai_functions import (
    create_structured_output_chain,
)
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage, BasePromptTemplate
from pydantic import BaseModel


M = TypeVar("M", bound=BaseModel)

# Taken from LangChain docs, need to validate that this is best.
prompt_msgs = [
    SystemMessage(
        content="You are a world class algorithm for extracting information in structured formats."
    ),
    HumanMessage(
        content="Use the given format to extract information from the following input:"
    ),
    HumanMessagePromptTemplate.from_template("{input}"),
    HumanMessage(content="Tips: Make sure to answer in the correct format"),
]
default_prompt = ChatPromptTemplate(messages=prompt_msgs)


def langchain_model(
    _cls=None,
    _llm: Optional[ChatOpenAI] = None,
    _prompt: Optional[BasePromptTemplate] = None,
    **kwargs: Any
) -> Callable[[Type[M]], Type[M]]:
    llm = _llm or ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    prompt = _prompt or default_prompt
    if _cls is None:

        def class_rebuilder(cls):
            chain = create_structured_output_chain(cls, llm, prompt, **kwargs)

            class NewClass(cls):
                def __init__(self, *args, **kwargs):
                    super().__init__(**chain.run(args[0]).dict())

            NewClass.__name__ = cls.__name__
            return NewClass

        return class_rebuilder
    else:
        chain = create_structured_output_chain(_cls, llm, prompt, **kwargs)

        class NewClass(_cls):
            def __init__(self, *args, **kwargs):
                super().__init__(**chain.run(args[0]).dict())

        NewClass.__name__ = _cls.__name__
        return NewClass
