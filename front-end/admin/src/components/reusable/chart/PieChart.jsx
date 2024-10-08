import { Chart as ChartJS, ArcElement, Legend, Title, Tooltip } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import PropTypes from 'prop-types';

ChartJS.register(ArcElement, Legend, Title, Tooltip);

function getRandomColor() {
    // Generates a random hex color code
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

function PieChart({ chartData }) {
    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: chartData.position || 'bottom',
            },
            title: {
                display: true,
                text: chartData.title,
            }
        }
    };

    const data = {
        labels: chartData.labels,
        datasets: chartData.datasets?.map((dataset) => ({
                label: dataset.label,
                data: dataset.data,
                backgroundColor: dataset.color ? dataset.color : dataset.data.map(() => getRandomColor()),
                hoverOffset: dataset.offset,
        })) || []
    };

    return (
        <div className='card chadow m-4 p-2'>
            <div className="card-header py-3">
                <h6 className="m-0 font-weight-bold text-primary text-center">{chartData.title}</h6>
            </div>
            <div className="card-body">
                <div className="chart-area">
                    <Pie options={options} data={data} />
                </div>
                <hr />
                {chartData.text}
            </div>
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
                    PropTypes.oneOf([
                        PropTypes.string,
                        PropTypes.number
                    ])
                ).isRequired,
                color: PropTypes.oneOfType([
                    PropTypes.string,
                    PropTypes.arrayOf(
                        PropTypes.string
                    ),
                ]).isRequired,
                offset: PropTypes.number.isRequired,
            }),
        ).isRequired,
        text: PropTypes.string,
    }).isRequired,
}

export default PieChart;
