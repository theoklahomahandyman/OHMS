import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Legend, Title, Tooltip } from 'chart.js';
import { Line } from 'react-chartjs-2';
import PropTypes from 'prop-types';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Legend, Title, Tooltip);

function LineChart({ chartData }) {
    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: chartData.position,
            },
            title: {
                display: true,
                text: chartData.title,
            }
        }
    };

    const data = {
        labels: chartData.labels,
        datasets: [
            chartData.datasets.map((dataset) => ({
                label: dataset.label,
                data: dataset.data,
                borderColor: dataset.color,
            }))
        ]
    };

    return (
        <div>
            <Line options={options} data={data} />
        </div>
    );
}

LineChart.propTypes = {
    chartData: PropTypes.shape({
        position: PropTypes.string.isRequired,
        title:  PropTypes.string.isRequired,
        labels: PropTypes.arrayOf(
            PropTypes.string
        ).isRequired,
        datasets: PropTypes.arrayOf(
            PropTypes.shape({
                label: PropTypes.string.isRequired,
                data: PropTypes.arrayOf(
                    PropTypes.oneOf(
                        PropTypes.string,
                        PropTypes.number
                    )
                ).isRequired,
                color: PropTypes.oneOf(
                    PropTypes.string,
                    PropTypes.arrayOf(
                        PropTypes.string
                    )
                ).isRequired,
            }),
        ).isRequired,
    }).isRequired,
}

export default LineChart;
