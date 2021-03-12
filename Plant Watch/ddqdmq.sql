----------DDQs--------------------
CREATE TABLE PlantAreas (
	areaID INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name varchar(255) NOT NULL
);

CREATE TABLE PlantStores (
    storeID INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    areaID INT,
    FOREIGN KEY (areaID)
    	REFERENCES PlantAreas(areaID),
    storeName varchar(255) NOT NULL,
    website TEXT,
    address TEXT,
    restockDay TEXT
    );

INSERT INTO PlantAreas (name)
VALUES
	('South Bay'),
		('North Bay'),
    ('East Bay'),
    ('Peninsula'),
    ('Online/Out of Bay');

INSERT INTO PlantStores (areaID, storeName, website, address, restockDay)
VALUES
    (5, 'Peace Love Happiness Club', 'https://peaceloveandhappiness.club/', 'Oregon', 'Daily'),
    (1, 'Gardeneur', 'https://www.gardeneur.com/', 'Depends on Seller', 'Mostly Sunday'),
    (5, 'Leafy Soulmates', 'https://leafysoulmates.com/', 'SoCal', 'Thursdays'),
    (3, 'California Plantin', 'https://californiaplantin.com/', '3791 Smith St, Union City', 'Wed & Fri'),
    (4, 'Leafy', 'https://www.leafypaloalto.com/', '482 Hamilton Ave, Palo Alto', 'Maybe Tues/Thurs');

-----------DMQs-----------------------

--Get tables - per area
SELECT PlantStores.*, PlantAreas.name FROM PlantStores
INNER JOIN PlantAreas ON PlantAreas.areaID = PlantStores.area
WHERE PlantStores.area = :areaIDInput;
-- all of the bay
SELECT PlantStores.*, PlantAreas.name FROM PlantStores
INNER JOIN PlantAreas ON PlantAreas.areaID = PlantStores.area;
WHERE PlantStores.area != 5;
--Insert store
INSERT INTO PlantStores (area, storeName, website, address, restockDay)
VALUES
    (:areaID, :storeNameInput, :websiteInput, :addressInput, :restockDayInput);

--Update store
UPDATE PlantStores
SET area = :areaIDInput,
    storeName = :storeNameInput,
    website = :websiteInput,
    address = :addressInput,
    restockDay = :restockDay
WHERE storeID = :storeIDInput;

--Delete store
DELETE FROM PlantStores WHERE storeID = :storeIDInput;
