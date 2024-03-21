import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

class DataOrganizer:
    def __init__(self):
        pass

    def load_data(self, file_path, file_format):
        """
        Load data from a file.

        Args:
            file_path (str): Path to the data file.
            file_format (str): Format of the data file (e.g., CSV, JSON, etc.).

        Returns:
            data: Loaded data.
        """
        if file_format == 'csv':
            data = pd.read_csv(file_path)
        elif file_format == 'json':
            data = pd.read_json(file_path)
        else:
            raise ValueError("Unsupported file format. Supported formats: 'csv', 'json'")
        
        return data

    def split_data(self, data, train_size, validation_size, test_size):
        """
        Split the data into training, validation, and testing sets.

        Args:
            data: Input data to split.
            train_size (float): Proportion of the data to include in the training set.
            validation_size (float): Proportion of the data to include in the validation set.
            test_size (float): Proportion of the data to include in the testing set.

        Returns:
            tuple: Three datasets - (train_data, validation_data, test_data).
        """
        remaining_size = 1.0 - (train_size + validation_size + test_size)
        if remaining_size < 0:
            raise ValueError("Sum of train_size, validation_size, and test_size cannot exceed 1.0")

        train_data, remaining_data = train_test_split(data, test_size=(validation_size + test_size), random_state=42)
        validation_data, test_data = train_test_split(remaining_data, test_size=test_size/(validation_size + test_size), random_state=42)

        return train_data, validation_data, test_data

    def preprocess_data(self, data, preprocessing_steps):
        """
        Preprocess the data using specified preprocessing steps.

        Args:
            data: Input data to preprocess.
            preprocessing_steps (list): List of preprocessing steps to apply.

        Returns:
            preprocessed_data: Preprocessed data.
        """
        preprocessed_data = data.copy()
        for step in preprocessing_steps:
            if step == 'remove_duplicates':
                preprocessed_data.drop_duplicates(inplace=True)
            elif step == 'handle_missing_values':
                preprocessed_data.dropna(inplace=True)
            elif step == 'standardize_features':
                scaler = StandardScaler()
                preprocessed_data.iloc[:, :-1] = scaler.fit_transform(preprocessed_data.iloc[:, :-1])
            elif step == 'encode_labels':
                label_encoder = LabelEncoder()
                preprocessed_data.iloc[:, -1] = label_encoder.fit_transform(preprocessed_data.iloc[:, -1])
            # Add more preprocessing steps as needed
            
        return preprocessed_data

    def save_data(self, data, file_path, file_format):
        """
        Save data to a file.

        Args:
            data: Data to save.
            file_path (str): Path to save the data file.
            file_format (str): Format of the data file (e.g., CSV, JSON, etc.).
        """
        if file_format == 'csv':
            data.to_csv(file_path, index=False)
        elif file_format == 'json':
            data.to_json(file_path, orient='records', lines=True)
        else:
            raise ValueError("Unsupported file format. Supported formats: 'csv', 'json'")
