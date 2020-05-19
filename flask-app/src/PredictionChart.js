import React, { Component } from 'react';
import { Chart, Line } from 'react-chartjs-2';
import facade from '../../apiFacade'
//import Loader from './Loader';

class PredictionChart extends Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: false,       
            data: {
                labels: [],
                datasets: []
            }
        }
    }
    
    componentDidMount() {
        Chart.pluginService.register({
            afterDraw: function (chart, easing) {
                if (chart.tooltip._active && chart.tooltip._active.length) {
                    const activePoint = chart.controller.tooltip._active[0];
                    const ctx = chart.ctx;
                    const x = activePoint.tooltipPosition().x;
                    const y = activePoint.tooltipPosition().y;
                    const bottomY = chart.scales['y-axis-0'].bottom;
                    ctx.save();
                    ctx.beginPath();
                    ctx.moveTo(x, y);
                    ctx.lineTo(x, bottomY);
                    ctx.lineWidth = 0.5;
                    ctx.strokeStyle = '#ACADBC';
                    ctx.stroke();
                    ctx.save();
                }
            }
        });
    }

    

    componentDidUpdate(prevProps) {
        if (prevProps.data !== this.props.data) {
            this.setState({
                data: this.props.data
            })
        }
        

    }



    render() {
        return (
            <div>

            </div>

        )
    }
}

export default PredictionChart;
