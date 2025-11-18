import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class Visualization:
    def create_score_chart(self, scores):
        """Create a score visualization chart"""
        df = pd.DataFrame({
            'Question': [f'Q{i+1}' for i in range(len(scores))],
            'Score': scores
        })
        
        fig = px.bar(df, x='Question', y='Score', 
                    title='Question-wise Performance',
                    color='Score',
                    color_continuous_scale='Viridis')
        
        fig.update_layout(
            yaxis=dict(range=[0, 10]),
            showlegend=False
        )
        
        return fig
    
    def create_ai_detection_gauge(self, ai_probability):
        """Create AI detection probability gauge"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = ai_probability * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "AI Content Probability"},
            delta = {'reference': 50},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        return fig