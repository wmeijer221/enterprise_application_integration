<!-- Svelte pie chart using tailwind -->
<script lang="ts">
	// import pie chart from chart.js
	import { Pie } from 'svelte-chartjs';
	import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale } from 'chart.js';

	export let positiveSentimentCount: number;
	export let negativeSentimentCount: number;

	ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

	$: data = {
		labels: ['Positive', 'Negative'],
		datasets: [
			{
				label: 'Count',
				data: [positiveSentimentCount, negativeSentimentCount],
				backgroundColor: ['#30BE39', '#BE4D30']
			}
		]
	};

	const options = {
		responsive: true,
		// size
		maintainAspectRatio: false,
		plugins: {
			legend: {
				position: 'bottom',
				labels: {
					color: '#fff',
					font: {
						size: 16
					}
				}
			},
			title: {
				display: true
			}
		}
	};
</script>

<Pie {data} {options} />
