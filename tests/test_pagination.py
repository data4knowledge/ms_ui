import pytest
from d4k_ms_ui.pagination import Pagination

def test_pagination_initialization():
    results = {
        'page': '1',
        'size': '10',
        'count': '25',
        'filter': ''
    }
    pagination = Pagination(results, '/test')
    
    assert pagination.page == 1
    assert pagination.page_size == 10
    assert pagination.item_count == 25
    assert pagination.page_count == 3
    assert pagination.base_url == '/test'
    assert pagination.filter == ''

def test_pagination_with_partial_page():
    results = {
        'page': '1',
        'size': '10',
        'count': '22',  # This should still result in 3 pages
        'filter': ''
    }
    pagination = Pagination(results, '/test')
    assert pagination.page_count == 3

def test_link_generation():
    results = {
        'page': '1',
        'size': '10',
        'count': '25',
        'filter': 'test'
    }
    pagination = Pagination(results, '/test')
    
    expected = '/test?page=2&size=10&filter=test'
    assert pagination.link(2) == expected

def test_link_with_additional_params():
    results = {
        'page': '1',
        'size': '10',
        'count': '25',
        'filter': ''
    }
    params = {'sort': 'desc', 'category': 'books'}
    pagination = Pagination(results, '/test', params=params)
    
    expected = '/test?page=2&size=10&filter=&sort=desc&category=books'
    assert pagination.link(2) == expected

def test_filter_disabled():
    results = {
        'page': '1',
        'size': '10',
        'count': '25',
        'filter': ''
    }
    pagination = Pagination(results, '/test', disable_filter=True)
    
    assert pagination.filter_disabled() == 'disabled'
    assert pagination.filter_text() == 'Search disabled!'

def test_autofocus():
    results = {
        'page': '1',
        'size': '10',
        'count': '25',
        'filter': 'test'
    }
    pagination = Pagination(results, '/test')
    
    assert pagination.autofocus() == 'autofocus'
    
    results['filter'] = ''
    pagination = Pagination(results, '/test')
    assert pagination.autofocus() == ''

def test_page_info_structure():
    results = {
        'page': '2',
        'size': '10',
        'count': '30',
        'filter': ''
    }
    pagination = Pagination(results, '/test')
    pages = pagination.pages
    
    # Check first and last elements (prev and next arrows)
    assert pages[0]['text'] == '&laquo;'
    assert pages[-1]['text'] == '&raquo;'
    
    # Check current page is marked active
    current_page = next(page for page in pages if page['active'] == 'active')
    assert current_page['text'] == '2'

def test_base_link_methods():
    results = {
        'page': '1',
        'size': '10',
        'count': '25',
        'filter': 'test'
    }
    pagination = Pagination(results, '/test')
    
    assert pagination.base_link(2, 20) == '/test?page=2&size=20'
    assert pagination.base_link_with_filter(2, 20) == '/test?page=2&size=20&filter=test' 