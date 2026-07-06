import pytest
from dash import Dash, html, dcc
import pandas as pd
from app import app, update_graph


class TestAppLayout:
    def test_app_exists(self):
        assert isinstance(app, Dash)
    
    def test_app_layout_not_none(self):
        assert app.layout is not None
    
    def test_header_exists(self):
        layout = app.layout
        assert any(isinstance(child, html.H1) for child in layout.children 
                   if hasattr(child, 'children'))
    
    def test_radio_items_component_exists(self):
        layout = app.layout
        radio_found = False
        for child in layout.children:
            if hasattr(child, 'children'):
                for sub_child in child.children:
                    if isinstance(sub_child, dcc.RadioItems):
                        radio_found = True
                        assert sub_child.id == "region-radio"
                        break
        assert radio_found, "RadioItems component not found"
    
    def test_graph_component_exists(self):
        layout = app.layout
        graph_found = False
        for child in layout.children:
            if hasattr(child, 'children'):
                for sub_child in child.children:
                    if isinstance(sub_child, dcc.Graph):
                        graph_found = True
                        assert sub_child.id == "sales-graph"
                        break
        assert graph_found, "Graph component not found"


class TestCallbackFunction:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.df = pd.read_csv('formatted_sales_data.csv')
        self.df = self.df.sort_values(by="date")
    
    def test_update_graph_with_all_regions(self):
        fig = update_graph("All")
        assert fig is not None
        assert "All Regions" in fig.layout.title.text
        assert fig.layout.xaxis.title.text == "Date"
        assert fig.layout.yaxis.title.text == "Sales ($)"
    
    def test_update_graph_with_specific_region(self):
        regions = self.df["region"].unique()
        if len(regions) > 0:
            region = regions[0]
            fig = update_graph(region)
            assert fig is not None
            assert region in fig.layout.title.text
            assert f"Sales Over Time - {region}" in fig.layout.title.text
    
    def test_graph_has_correct_layout_properties(self):
        fig = update_graph("All")
        assert fig.layout.template is not None
        assert fig.layout.template.layout.paper_bgcolor == "white"
        assert fig.layout.xaxis.title.text == "Date"
        assert fig.layout.yaxis.title.text == "Sales ($)"
    
    def test_graph_has_markers(self):
        fig = update_graph("All")
        has_markers = any(trace.mode == 'lines+markers' for trace in fig.data)
        assert has_markers or any('markers' in str(trace.mode) for trace in fig.data)


class TestDataLoading:
    def test_data_is_loaded(self):
        df = pd.read_csv('formatted_sales_data.csv')
        assert df is not None
        assert len(df) > 0
    
    def test_data_has_required_columns(self):
        df = pd.read_csv('formatted_sales_data.csv')
        required_columns = ['date', 'sales', 'region']
        for col in required_columns:
            assert col in df.columns, f"Column '{col}' not found in data"
    
    def test_data_is_sorted_by_date(self):
        df = pd.read_csv('formatted_sales_data.csv')
        df_sorted = df.sort_values(by="date")
        pd.testing.assert_frame_equal(df, df_sorted, check_like=True)


class TestRadioItemsOptions:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.df = pd.read_csv('formatted_sales_data.csv')
    
    def test_radio_items_has_all_regions_option(self):
        layout = app.layout
        for child in layout.children:
            if hasattr(child, 'children'):
                for sub_child in child.children:
                    if isinstance(sub_child, dcc.RadioItems):
                        options = sub_child.options
                        assert any(opt['value'] == 'All' for opt in options)
                        assert any('All Regions' in opt['label'] for opt in options)
    
    def test_radio_items_default_value_is_all(self):
        layout = app.layout
        for child in layout.children:
            if hasattr(child, 'children'):
                for sub_child in child.children:
                    if isinstance(sub_child, dcc.RadioItems):
                        assert sub_child.value == "All"
    
    def test_radio_items_includes_all_regions_from_data(self):
        regions = self.df["region"].unique()
        layout = app.layout
        for child in layout.children:
            if hasattr(child, 'children'):
                for sub_child in child.children:
                    if isinstance(sub_child, dcc.RadioItems):
                        option_values = [opt['value'] for opt in sub_child.options]
                        for region in regions:
                            assert region in option_values


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
