import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Legend, Title, Tooltip } from 'chart.js';
import { Bar } from 'react-chartjs-2';
import PropTypes from 'prop-types';

ChartJS.register(CategoryScale, LinearScale, BarElement, Legend, Title, Tooltip);

function BarChart({ chartData }) {
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
                backgroundColor: dataset.background,
                borderColor: dataset.color,
                borderWidth: 1,
            }))
        ]
    };

    return (
        <div>
            <Bar options={options} data={data} />
        </div>
    );
}

BarChart.propTypes = {
    chartData: PropTypes.shape({
        position: PropTypes.string.isRequired,
        title: PropTypes.string.isRequired,
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
                background: PropTypes.oneOf(
                    PropTypes.string,
                    PropTypes.arrayOf(
                        PropTypes.string
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

export default BarChart;
