import { Chart as ChartJS, ArcElement, Legend, Title, Tooltip } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import PropTypes from 'prop-types';

ChartJS.register(ArcElement, Legend, Title, Tooltip);

function PieChart({ chartData }) {
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
                backgroundColor: dataset.color,
                hoverOffset: dataset.offset,
            }))
        ]
    };

    return (
        <div>
            <Pie options={options} data={data} />
        </div>
    );
}

PieChart.propTypes = {
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
                color: PropTypes.oneOf(
                    PropTypes.string,
                    PropTypes.arrayOf(
                        PropTypes.string
                    )
                ).isRequired,
                offset: PropTypes.number.isRequired,
            }),
        ).isRequired,
    }).isRequired,
}

export default PieChart;
