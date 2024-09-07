import React from 'react';
import CalendarHeatmap from 'react-calendar-heatmap';
// import ReactTooltip from 'react-tooltip';
import 'react-calendar-heatmap/dist/styles.css';
import { Box, Typography } from '@mui/material';

interface ReviewCount {
  date: string;
  count: number;
}

interface ReviewHeatmapProps {
  reviewCounts: ReviewCount[];
}

// const reviewCounts: ReviewCount[] = [
//     { date: '2023-05-01', count: 3 },
//     { date: '2023-05-02', count: 7 },
//     { date: '2023-05-03', count: 12 },
//     { date: '2023-05-04', count: 18 },
//     { date: '2023-05-05', count: 25 },
//     { date: '2023-05-10', count: 5 },
//     { date: '2023-05-15', count: 10 },
//     { date: '2023-05-20', count: 15 },
//     { date: '2023-05-25', count: 20 },
//     { date: '2023-05-30', count: 30 },
//   ];

const ReviewHeatmap: React.FC<ReviewHeatmapProps> = ({ reviewCounts }) => {
  /**
   * ReviewHeatmap Component
   *
   * This component renders a heatmap visualization of review activity over the past year.
   * It uses the react-calendar-heatmap library to create a GitHub-style contribution graph.
   *
   * @param {ReviewCount[]} reviewCounts - An array of objects containing date and review count data.
   * Each object should have a 'date' string (YYYY-MM-DD format) and a 'count' number.
   *
   * The heatmap color intensity is determined by the number of reviews on each day:
   * - 0 reviews: Empty (default color)
   * - 1-5 reviews: Lightest green
   * - 6-10 reviews: Light green
   * - 11-15 reviews: Medium green
   * - 16-20 reviews: Dark green
   * - 20+ reviews: Darkest green
   *
   * The component also includes a tooltip that displays the date and number of reviews when hovering over a cell.
   */

  // Use the example data instead of the prop
  // const reviewData = exampleReviewCounts;
  const today = new Date();
  const startDate = new Date(today.getFullYear(), today.getMonth() - 11, 1);

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h6" gutterBottom>
        Review Heatmap
      </Typography>
      <CalendarHeatmap
        startDate={startDate}
        endDate={today}
        values={reviewCounts}
        classForValue={(value) => {
          if (!value) {
            return 'color-empty';
          }
          return `color-scale-${Math.min(Math.floor(value.count / 5), 4)}`;
        }}
        tooltipDataAttrs={(value: ReviewCount | null) => {
          if (!value || !value.date) {
            return null;
          }
          return {
            'data-tip': `${value.date}: ${value.count} reviews`,
          };
        }}
      />
      {/* <style jsx global>{`
        .react-calendar-heatmap .color-scale-0 {
          fill: #d6e685;
        }
        .react-calendar-heatmap .color-scale-1 {
          fill: #8cc665;
        }
        .react-calendar-heatmap .color-scale-2 {
          fill: #44a340;
        }
        .react-calendar-heatmap .color-scale-3 {
          fill: #1e6823;
        }
        .react-calendar-heatmap .color-scale-4 {
          fill: #0e4c14;
        }
      `}</style> */}
    </Box>
  );
};

export default ReviewHeatmap;
