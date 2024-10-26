# Takes in condition from user, spits out dictionary

def add_condition (
            self_conditions: list,
            self_downloads: list,
            self_studies: list,
            name: str,
            ticker_1: str = None,
            study_1: str = None, 
            ticker_2: str = None,
            study_2: str = None,
            operator: str = None,
            study_1_period: int = None,
            study_2_period: int = None,
            study_1_short_period: int = None,
            study_2_short_period: int = None,
            study_1_long_period: int = None,
            study_2_long_period: int = None,
            study_1_period_type: str = None,
            study_2_period_type: str = None,
            value: float = None
            
    ) -> dict:
        '''Function reads ticker_1 -> operator -> ticker_2'''
        def validate_name():
            if len(self_conditions) > 0:
                for condition in self_conditions:
                    if name in condition['name']:
                        raise ValueError("Each condition's name must be unique!")

            return name

        def validate_tickers(
                ticker_1 = ticker_1,
                ticker_2 = ticker_2
        ):

            if ticker_1 is None:
                raise ValueError("Ticker_1 cannot be blank!")
            
            if ticker_2 is None:
                if study_2 is not None:
                    raise ValueError('ticker_2 cannot be blank if study_2 is blank!')
                else:
                    return {
                        'ticker_1': ticker_1.upper(),
                        'ticker_2': None
                    }
            else:
                return {
                    'ticker_1': ticker_1.upper(),
                    'ticker_2': ticker_2.upper()
                }                
            
        def validate_studies(
            study_1=study_1,
            study_2=study_2
        ):
            study_list = [study_1, study_2]

            if study_1 is None:
                raise ValueError("Study_1 cannot be blank!")
            
            if study_2 is None:
                study_list.remove(study_2)
                
            if study_1.upper() == 'PRICE':
                study_1 = study_1.capitalize()
            else:
                study_1 = study_1.upper()

            if study_2 is not None:
                if study_2.upper() == 'PRICE':
                    study_2 = study_2.capitalize()
                else:
                    study_2 = study_2.upper()

            function_dict = {
                'study_1': study_1,
                'study_2': study_2
            }

            return function_dict

        def validate_operator(
            operator=operator
        ):
            supported_list = [
                '>',
                '<',
                '==',
                '>=',
                '<='
            ]

            if operator not in supported_list:
                raise ValueError("Operator is not supported!")
            return operator

        def validate_period_types (
                type_1 = study_1_period_type,
                type_2 = study_2_period_type
        ):
            type_list = [type_1, type_2]

            if type_1 is None:
                type_1 = 'Close'
                type_list[0] = type_1
            else:
                type_1 = type_1.capitalize()
                type_list[0] = type_1
                
            if validate_studies()['study_2'] is None:
                type_list.remove(type_2)
                if type_2 is not None:
                    raise ValueError(
                        'study_2_period_type must be blank if study_2 is blank!'
                    )

            elif validate_studies()['study_2'] is not None:
                if type_2 is None:
                    type_2 = 'Close'
                    type_list[1] = type_2

            types = [
                'High', 'Low', 'Close'
            ]
    
            for type_x in type_list:
                if type_x not in types:
                    raise ValueError (f"type_x is not valid, ensure type is either Close, High, or Low!")
            
            if type_2 is not None:
                type_2 = type_2.capitalize()
            return {
                'type_1': type_1, 
                'type_2': type_2
            }
        
        def validate_value():
            if value is not None:
                if validate_tickers()['ticker_2'] is not None:
                    raise ValueError('Value must be blank if Ticker_2 is used!')
                if validate_studies()['study_2'] is not None:
                    raise ValueError('Value must be blank if study_2 is used!')
            return value

        def validate_periods():
            if study_1_period is not None and study_1.upper() == 'PRICE':
                raise ValueError('study_1_period must be blank if study_1 is PRICE!')
            if study_2_period is not None and study_2.upper() == 'PRICE':
                raise ValueError('study_2_period must be blank if the study is PRICE!')
            valid_periods = {
                'study_1_period': study_1_period,
                'study_2_period': study_2_period,
                'study_1_short_period': study_1_short_period,
                'study_2_short_period': study_2_short_period,
                'study_1_long_period': study_1_long_period,
                'study_2_long_period': study_2_long_period
            }
            return valid_periods

        def return_condition_list():
            condition_dict = {
                'name': validate_name(),
                'ticker_1': validate_tickers()['ticker_1'],
                'study_1': validate_studies()['study_1'],
                'ticker_2': validate_tickers()['ticker_2'],
                'study_2': validate_studies()['study_2'],
                'operator': validate_operator(),
                'study_1_period': validate_periods()['study_1_period'],
                'study_2_period': validate_periods()['study_2_period'],
                'study_1_short_period': validate_periods()['study_1_short_period'],
                'study_2_short_period': validate_periods()['study_2_short_period'],
                'study_1_long_period': validate_periods()['study_1_long_period'],
                'study_2_long_period': validate_periods()['study_2_long_period'],
                'study_1_period_type': validate_period_types()['type_1'],
                'study_2_period_type': validate_period_types()['type_2'],
                'value': validate_value()
            }
            self_conditions.append(condition_dict)
            return self_conditions
        
        def return_download_list():
            download_dict = {
                'download_1': [validate_tickers()['ticker_1'], validate_period_types()['type_1']],
                'download_2': [validate_tickers()['ticker_2'], validate_period_types()['type_2']]
            }

            new_downloads = []
            for download in download_dict.keys():
                
                if download_dict[download] not in self_downloads and download_dict[download][0] is not None:
                    self_downloads.append(download_dict[download])
                    new_downloads.append(download_dict[download])

            return {
                'self_downloads': self_downloads,
                'new_downloads': new_downloads
            }
        
        def return_study_list():
            tickers = validate_tickers()
            studies = validate_studies()
            periods = validate_periods()
            types = validate_period_types()
            value = validate_value()

            my_dict_1 = {
                'ticker': tickers['ticker_1'],
                'study': studies['study_1'],
                'study_period': periods['study_1_period'],
                'short_period': periods['study_1_short_period'],
                'long_period': periods['study_1_long_period'],
                'period_type': types['type_1'],
                'value': 0
            }
            my_dict_2 = {
                'ticker': tickers['ticker_2'],
                'study': studies['study_2'],
                'study_period': periods['study_2_period'],
                'short_period': periods['study_2_short_period'],
                'long_period': periods['study_2_long_period'],
                'period_type': types['type_2'],
                'value': value
            }
            new_studies = []
            for my_dict in (my_dict_1, my_dict_2):
                if my_dict not in self_studies:
                    self_studies.append(my_dict)
                    new_studies.append(my_dict)
            return {
                'self_studies': self_studies,
                'new_studies': new_studies
            }
        
        studies = return_study_list()
        downloads = return_download_list()
        conditions = return_condition_list()

        return_dict = {
            'studies': studies['self_studies'],
            'new_studies': studies['new_studies'],
            'downloads': downloads['self_downloads'],
            'new_downloads': downloads['new_downloads'],
            'conditions': conditions,
            'new_downloads': downloads['new_downloads']
        }


        return return_dict


