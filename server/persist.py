# File Name: persist.py
# File Description: persist layer of the reserve system
#
# Date: May 7, 2022

class DataManager:
    def __init__(self, data_file):
        self.data_file = data_file
        self.r_manager = ReservationManager()
        self.t_manager = TransactionManager()
        self.load_data()
    
    def load_data(self):
        """
        Load data from data file to the DataManager
        """
        file = open(self.data_file, 'r')
        lines = file.readlines()
        # Read every line from data file, with a hash # seperating the reservations
        # from the transactions
        convert_to_reservation = True
        for line in lines:
            line = line.split()
            if line[0] == '#':
                convert_to_reservation = False
                continue
            if convert_to_reservation:
                self.r_manager.add_data(Reservation(line))
            else:
                self.t_manager.add_data(Transaction(line))
        file.close()
    

    def close(self):
        """
        Save data in the DataManager to data file
        """
        # save_to_file reservation and transaction data, seperated by a hash #
        file = open(self.data_file, 'w')
        self.r_manager.save(file)
        file.write('#\n')
        self.t_manager.save(file)
        file.close()

    
    def max_reservation_id(self):
        """
        Return the max reservation id

        Returns: 
            an integer
        """
        return self.r_manager.max_id()
    
    def max_transaction_id(self):
        """
        Return the max transaction id

        Returns: 
            an integer
        """
        return self.t_manager.max_id()

    def add_reservation(self, reservation):
        """
        Add a reservation

        Args:
            reservation (Reservation): reservation to add
        """
        self.r_manager.add_data(reservation)
    
    def add_transaction(self, transaction):
        """
        Add a transaction

        Args:
            transaction (Transaction): transaction to add
        """
        self.t_manager.add_data(transaction)
    
    def all_reservations(self):
        """
        Return all reservations

        Returns:
            A list of reservations (List[Reservation])
        """
        return self.r_manager.data
    
    def all_transactions(self):
        """
        Return all transactions

        Returns:
            A list of transactions (List[Transaction])
        """
        return self.t_manager.data
    
    def select_reservation(self, reservation_id):
        """
        Return a certain reservation
        
        Args:
            reservation_id (int)

        Returns:
            A reservation (Reservation)
        """
        return self.r_manager.select_reservation(reservation_id)

    def delete_reservation(self, reservation_id):
        """
        Delete a certain reservation
        
        Args:
            reservation_id (int)
        """
        self.r_manager.delete_reservation(reservation_id)


class Reservation:
    """
    A class representing a single reservation within the system

    All dates stored are in the form of a mm-dd-yyyy string
    Attributes:
        reservation_id (int): A unique interger for each reservation
        customer_id (str): The unique string id representing a customer
        reservation_type (str): The type of reservation made (for workshop,
            or for a special machine)
        start_date (str): The starting date of the reservation 
        end_date (str): The ending date of the reservation
        date_of_reservation (str): The date on which the reservation is made
        total (float): A float representing the total cost of this reservation
        down_payment (float): A float representing the amount required for a down payment
        reservation_string (str): A string representation of the reservation object
    """
    def __init__(self, _reserve):
        self.reservation_id = int(_reserve[0])
        self.customer_id = _reserve[1]
        self.reservation_type = _reserve[2]
        self.start_date = _reserve[3]
        self.end_date = _reserve[4]
        self.start_time = _reserve[5]
        self.end_time = _reserve[6]
        self.date_of_reservation = _reserve[7]
        self.total_cost = float(_reserve[8])
        self.down_payment = float(_reserve[9])
        self.data_string = ' '.join(_reserve)
    
    def tolist(self):
        """
        Convert all information in the Reservation object to a list object

        Returns:
            A string that includes all information about the Reservation object
        """
        return [str(self.reservation_id), self.customer_id, self.reservation_type,
                    self.start_date, self.end_date, self.start_time, self.end_time,
                    self.date_of_reservation, str(self.total_cost), str(self.down_payment)]

    
class Transaction:
    """
    A class representing transactions that have taken place in the system

    Attributes:
        transaction_id (int): A unique interger for each transaction
        type (str): The type of transaction (CANCELLATION or RESERVATION)
        transaction_date (str): Date of the transaction in mm-dd-yyyy format
        detail (Reservation): The Reservation object related to this transaction
        transaction_string (str): A string representation of the reservation
            related to this transaction
    """
    def __init__(self, transaction):
        self.transaction_id = int(transaction[0])
        self.type = transaction[1]
        self.transaction_date = transaction[2]
        self.detail = Reservation(transaction[3:13])
        self.data_string = f'{self.transaction_id} {self.type} {self.transaction_date} {self.detail.data_string} {transaction[-2]} {transaction[-1]}'


class Manager:
    """
    Attributes:
        data (List): A list that contains data
    """
    def __init__(self):
        self.data = []
    
    def add_data(self, data):
        """
        Add data

        Args:
            data: data to add
        """
        self.data.append(data)
    
    def save(self, file):
        """
        Write all data to the designated file descriptor

        Args:
            file (file descriptor)
        """
        for data in self.data:
            file.write(data.data_string)
            file.write('\n')


class ReservationManager(Manager):
    """
    A class to manage all the reservations within the system
    """

    def max_id(self):
        """
        Return the max id

        Returns:
            A Integer
        """
        if len(self.data) == 0:
            return 0
        return self.data[-1].reservation_id
        
    def select_reservation(self, reservation_id):
        """
        Return a certain reservation
        
        Args:
            reservation_id (int)

        Returns:
            A reservation (Reservation) or None if not found
        """
        for i in range(len(self.data)):
            if self.data[i].reservation_id == reservation_id:
                return self.data[i]
        return None
    
    def delete_reservation(self, reservation_id):
        """
        Delete a certain reservation
        
        Args:
            reservation_id (int)
        """
        for i in range(len(self.data)):
            if self.data[i].reservation_id == reservation_id:
                del self.data[i]
                break


class TransactionManager(Manager):
    """
    A class to manage all the transaction within the system
    """
    
    def max_id(self):
        """
        Return the max id

        Returns:
            A Integer
        """
        return len(self.data)