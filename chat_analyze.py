import re
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

from config.base_config import BaseConfig


class ChatAnalyzer:
    """
    Analyzes WhatsApp chat data.
    """
    date_time_format: str = BaseConfig.DATE_TIME_FORMAT
    chat_file_path: str = BaseConfig.CHAT_FILE_PATH

    def parse_chat(self, file_path):
        """
        Parses the WhatsApp chat export file.

        Args:
            file_path (str): Path to the WhatsApp chat text file.

        Returns:
            pd.DataFrame: DataFrame containing datetime, user, and message.
        """
        # Updated regex pattern to match the new format
        pattern = r'^\[(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}:\d{2})\]\s([^:]+):\s(.*)'
        messages = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                match = re.match(pattern, line)
                if match:
                    date_str = f"{match.group(1)}, {match.group(2)}"
                    try:
                        date_time = datetime.strptime(date_str, self.date_time_format)
                    except ValueError:
                        continue  # Skip lines that don't match the date format
                    user = match.group(3).strip()
                    message = match.group(4).strip()
                    messages.append({'datetime': date_time, 'user': user, 'message': message})
                else:
                    # Handle multi-line messages
                    if messages:
                        messages[-1]['message'] += '\n' + line.strip()
            df = pd.DataFrame(messages)
        return df

    def analyze_workouts(self, df: pd.DataFrame):
        """
        Analyzes workout entries in the DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing chat data.

        Returns:
            pd.DataFrame: DataFrame with workout dates per user.
        """
        # Updated to search for the '✅' emoji
        workout_df = df[df['message'].str.contains('✅')]
        workout_df['date'] = workout_df['datetime'].dt.date
        return workout_df.drop_duplicates(subset=['user', 'date'])

    def analyze_weights(self, df: pd.DataFrame):
        """
        Analyzes average weekly weights per user.

        Args:
            df (pd.DataFrame): DataFrame containing chat data.

        Returns:
            pd.DataFrame: DataFrame with average weights per week per user.
        """
        weight_pattern = r'average weight[:\-]?\s*(\d+\.?\d*)'
        weights = []
        for _, row in df.iterrows():
            match = re.search(weight_pattern, row['message'], re.IGNORECASE)
            if match:
                weight = float(match.group(1))
                week = row['datetime'].isocalendar()[1]
                year = row['datetime'].year
                weights.append({'year': year, 'week': week, 'user': row['user'], 'weight': weight})
        weight_df = pd.DataFrame(weights)
        weight_df = weight_df.groupby(['user', 'year', 'week']).mean().reset_index()
        return weight_df

    def plot_workouts(self, workout_df: pd.DataFrame):
        """
        Plots the workout days per user.

        Args:
            workout_df (pd.DataFrame): DataFrame with workout dates per user.
        """
        users = workout_df['user'].unique()
        for user in users:
            user_df = workout_df[workout_df['user'] == user]
            plt.figure(figsize=(10, 5))
            plt.plot(user_df['date'], [1] * len(user_df), 'o')
            plt.yticks([])
            plt.title(f'Workout Days for {user}')
            plt.xlabel('Date')
            plt.tight_layout()
            plt.show()

    def plot_weights(self, weight_df: pd.DataFrame):
        """
        Plots the average weekly weights per user.

        Args:
            weight_df (pd.DataFrame): DataFrame with average weights per week per user.
        """
        users = weight_df['user'].unique()
        for user in users:
            user_df = weight_df[weight_df['user'] == user]
            user_df['week_start'] = user_df.apply(
                lambda row: datetime.strptime(f'{row.year} {row.week} 1', '%G %V %u'), axis=1)
            plt.figure(figsize=(10, 5))
            plt.plot(user_df['week_start'], user_df['weight'], marker='o')
            plt.title(f'Average Weekly Weight for {user}')
            plt.xlabel('Week Starting')
            plt.ylabel('Weight')
            plt.tight_layout()
            plt.show()

    def flow(self):
        # Parse the chat file
        df = self.parse_chat(self.chat_file_path)

        # Analyze workouts
        workout_df = self.analyze_workouts(df)
        print("Workout Analysis:")
        print(workout_df)

        # Analyze weights
        weight_df = self.analyze_weights(df)
        print("\nWeight Analysis:")
        print(weight_df)

        # Plot the workouts
        self.plot_workouts(workout_df)

        # Plot the weights
        self.plot_weights(weight_df)


if __name__ == '__main__':
    analyzer = ChatAnalyzer()
    analyzer.flow()
