DROP DATABASE IF EXISTS PokerTournament;
CREATE DATABASE PokerTournament;
USE PokerTournament;

CREATE TABLE Players(
	player_id INT AUTO_INCREMENT PRIMARY KEY, 
	name VARCHAR(60) NOT NULL, 
	psu_email VARCHAR(30) UNIQUE NOT NULL,
	status VARCHAR(20)
);

CREATE TABLE Tournaments(
	tournament_id INT AUTO_INCREMENT PRIMARY KEY, 
	name VARCHAR(100), 
	Description VARCHAR(256), 
	organizer_id INT, 
    starting_chips INT,
	FOREIGN KEY (organizer_id) REFERENCES Players(player_id)
);

CREATE TABLE Registration(
	registration_id INT AUTO_INCREMENT PRIMARY KEY, 
	registered_player_id INT, 
	registered_tournament_id INT, 
	buyin_amount DECIMAL(12,2),
registered_status VARCHAR(20), 
FOREIGN KEY (registered_player_id) REFERENCES Players(player_id),
FOREIGN KEY (registered_tournament_id) REFERENCES Tournaments(tournament_id)
);

CREATE TABLE Tables(
	table_id INT AUTO_INCREMENT PRIMARY KEY, 
	table_tournament_id INT, 
	table_number INT, 
	max_seats INT, 
	player_registration_status VARCHAR(20), 
	FOREIGN KEY (table_tournament_id) REFERENCES Tournaments(tournament_id)
);

CREATE TABLE SeatingAssignments(
	seating_id INT AUTO_INCREMENT PRIMARY KEY, 
	seating_tournament_id INT, 
	seating_table_id INT, 
	seating_player_id INT, 
	seat_number INT, 
	FOREIGN KEY (seating_tournament_id) REFERENCES Tournaments(tournament_id),
	FOREIGN KEY (seating_player_id) REFERENCES Players(player_id),
	FOREIGN KEY (seating_table_id) REFERENCES Tables(table_id)
);

CREATE TABLE Games(
	game_id INT AUTO_INCREMENT PRIMARY KEY, 
	game_tournament_id INT, 
	game_table_id INT, 
	hand_number INT, 
	dealer_seat_number INT, 
	pot_amount DECIMAL(12,2), 
	FOREIGN KEY (game_tournament_id) REFERENCES Tournaments(tournament_id), 
	FOREIGN KEY (game_table_id) REFERENCES Tables(table_id)
);

CREATE TABLE GameActions(
	game_action_id INT AUTO_INCREMENT PRIMARY KEY, 
	game_action_game_id INT, 
	game_player_id INT, 
	action_type VARCHAR(20), 
	action_value DECIMAL(12,2),
	chips_removed INT, 
	FOREIGN KEY (game_action_game_id) REFERENCES Games(game_id), 
	FOREIGN KEY (game_player_id) REFERENCES Players(player_id)
);

CREATE TABLE Chips(
	chip_id INT AUTO_INCREMENT PRIMARY KEY, 
	chip_player_id INT, 
	chip_tournament_id INT, 
	chip_balance INT, 
	FOREIGN KEY (chip_player_id) REFERENCES Players(player_id),
	FOREIGN KEY (chip_tournament_id) REFERENCES Tournaments(tournament_id) 

);

CREATE TABLE Eliminations(
	elimination_id INT AUTO_INCREMENT PRIMARY KEY, 
	eliminated_player_id INT, 
	eliminated_tournament_id INT, 
	elimination_round INT, 
	position INT, 
FOREIGN KEY (eliminated_player_id) REFERENCES Players(player_id),
	FOREIGN KEY (eliminated_tournament_id) REFERENCES Tournaments(tournament_id)
);

CREATE TABLE Leaderboard(
	leaderboard_id INT AUTO_INCREMENT PRIMARY KEY, 
	leaderboard_tournament_id INT, 
	leaderboard_player_id INT, 
	current_chips INT, 
	wins INT,
	current_position INT, 
	FOREIGN KEY (leaderboard_player_id) REFERENCES Players(player_id),
	FOREIGN KEY (leaderboard_tournament_id) REFERENCES Tournaments(tournament_id)
);

-- Sample Data Injection

-- 1. Create Players
INSERT INTO Players (name, psu_email, status) VALUES 
('Lucas', 'lucas@psu.edu', 'Active'),
('Ehsaas', 'sus@psu.edu', 'Active'),
('James', 'james@psu.edu', 'Active');

-- 2. Create a Tournament (Organized by Lucas)
INSERT INTO Tournaments (name, Description, organizer_id) VALUES 
('PSU Friday Night', 'Weekly main event', 1);

-- 3. Register Players (Buyin: 500)
INSERT INTO Registration (registered_player_id, registered_tournament_id, buyin_amount, registered_status) VALUES 
(1, 1, 500.00, 'Registered'),
(2, 1, 500.00, 'Registered'),
(3, 1, 500.00, 'Registered');

-- 4. Create a Table (Table 1)
INSERT INTO Tables (table_tournament_id, table_number, max_seats, player_registration_status) VALUES 
(1, 1, 6, 'Open');

-- 5. Seat the Players
INSERT INTO SeatingAssignments (seating_tournament_id, seating_table_id, seating_player_id, seat_number) VALUES 
(1, 1, 1, 1),
(1, 1, 2, 2),
(1, 1, 3, 3); 

-- 6. Initialize Player Chip Stacks (Starting with 1000)
INSERT INTO Chips (chip_player_id, chip_tournament_id, chip_balance) VALUES 
(1, 1, 1000),
(2, 1, 1000),
(3, 1, 1000);

-- 7. Start a Dummy Game (Hand #1)
INSERT INTO Games (game_tournament_id, game_table_id, hand_number, dealer_seat_number, pot_amount) VALUES 
(1, 1, 1, 1, 75.00); -- Dealer at Seat 1, Pot 75 (Blinds 25/50)

