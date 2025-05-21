-- Create table
CREATE TABLE inventory (
    item text NOT NULL,
    description text,
    price float NOT NULL,
	PRIMARY KEY (item)
);

-- Primary & Foreign Keys
CREATE TABLE transactions (
    transaction_id uuid DEFAULT gen_random_uuid() NOT NULL,  -- Note that the default transaction id is a randomly generated uuid
	item text NOT NULL,
    quantity int NOT NULL,
	PRIMARY KEY (transaction_id),
	FOREIGN KEY (item) REFERENCES inventory(item)
);

-- Insert
INSERT INTO inventory (item, description, price)
VALUES ('T-shirt', 'Black & white stripy t-shirt.', 12.99), ('Hoodie', 'Bright orange hoodie', 20.99)