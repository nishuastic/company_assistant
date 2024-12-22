import pytest
from app.utils.value_utils import (
    crawl_homepage,
    analyze_titles_with_openai,
    fetch_and_filter_relevant_pages,
    process_value_app_logic,
    query_vectorstore,
)
from unittest.mock import Mock, patch

MOCK_BASE_URL = "https://mocksite.com"
MOCK_PAGES = [
    {"url": "https://mocksite.com/about-us", "title": "About Us"},
    {"url": "https://mocksite.com/pricing", "title": "Pricing"},
]
MOCK_RELEVANT_TITLES = ["About Us", "Pricing"]
MOCK_CONTENT = {
    "https://mocksite.com/about-us": "About us content",
    "https://mocksite.com/pricing": "Pricing content",
}


# Test for crawl_homepage
def test_crawl_homepage(mocker):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = """
        <a href="/about-us">About Us</a>
        <a href="/pricing">Pricing</a>
    """
    mocker.patch("requests.get", return_value=mock_response)

    result = crawl_homepage(MOCK_BASE_URL)
    expected_result = [
        {"url": "https://mocksite.com/about-us", "title": "About Us"},
        {"url": "https://mocksite.com/pricing", "title": "Pricing"},
    ]
    assert result == expected_result


# Test for analyze_titles_with_openai
def test_analyze_titles_with_openai(mocker):
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="About Us, Pricing"))]
    mocker.patch(
        "app.utils.value_utils.client.chat.completions.create",
        return_value=mock_response,
    )

    result = analyze_titles_with_openai(["About Us", "Pricing", "Careers"])
    assert result == "About Us, Pricing"


# Test for fetch_and_filter_relevant_pages
def test_fetch_and_filter_relevant_pages(mocker):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "This is the content of the page."
    mocker.patch("requests.get", return_value=mock_response)

    result = fetch_and_filter_relevant_pages(
        MOCK_BASE_URL, MOCK_RELEVANT_TITLES, MOCK_PAGES
    )
    expected_result = {
        "https://mocksite.com/about-us": "This is the content of the page.",
        "https://mocksite.com/pricing": "This is the content of the page.",
    }
    assert result == expected_result


# Test for process_value_app_logic
def test_process_value_app_logic(mocker):
    mocker.patch("app.utils.value_utils.crawl_homepage", return_value=MOCK_PAGES)
    mocker.patch(
        "app.utils.value_utils.analyze_titles_with_openai",
        return_value=MOCK_RELEVANT_TITLES,
    )
    mocker.patch(
        "app.utils.value_utils.fetch_and_filter_relevant_pages",
        return_value=MOCK_CONTENT,
    )

    result = process_value_app_logic(MOCK_BASE_URL)
    assert result == MOCK_CONTENT


# Test for query_vectorstore
def test_query_vectorstore(mocker):
    mock_vectorstore = Mock()
    mock_vectorstore.similarity_search.return_value = [
        Mock(page_content="This is a mock response content."),
        Mock(page_content="Another piece of mock response content."),
    ]
    mock_response = Mock()
    mock_response.choices = [
        Mock(message=Mock(content="Here is the summarized content."))
    ]
    mocker.patch(
        "app.utils.value_utils.client.chat.completions.create",
        return_value=mock_response,
    )

    result = query_vectorstore(mock_vectorstore, "What is the pricing model?")
    assert result == "Here is the summarized content."
