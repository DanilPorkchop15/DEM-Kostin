-- создание и подключение к БД
CREATE DATABASE `partners_production_company` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE partners_production_company;

-- создание таблицы типов партнеров
CREATE TABLE `partners_production_company`.`partner_types` (
  `partner_type_id` INT UNIQUE NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`partner_type_id`));

-- создание таблицы партнеров
CREATE TABLE `partners_production_company`.`partners` (
  `partner_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `phone` VARCHAR(255) NOT NULL,
  `address` VARCHAR(255) NOT NULL,
  `inn` VARCHAR(15) NOT NULL,
  `rating` INT NULL,
  `partner_type_id` INT NOT NULL,
  PRIMARY KEY (`partner_id`),
  UNIQUE INDEX `partner_id_UNIQUE` (`partner_id` ASC) VISIBLE,
  INDEX `partner_type_id_idx` (`partner_type_id` ASC) VISIBLE,
  CONSTRAINT `partner_type_id`
    FOREIGN KEY (`partner_type_id`)
    REFERENCES `partners_production_company`.`partner_types` (`partner_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- создание таблицы типов продуктов
CREATE TABLE `partners_production_company`.`product_types` (
  `product_type_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `coef` FLOAT NOT NULL,
  PRIMARY KEY (`product_type_id`),
  UNIQUE INDEX `product_type_id_UNIQUE` (`product_type_id` ASC) VISIBLE);

-- создание таблицы продуктов
CREATE TABLE `partners_production_company`.`products` (
  `product_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `articul` VARCHAR(255) NOT NULL,
  `min_cost_for_partner` FLOAT NOT NULL,
  `product_type_id` INT NOT NULL,
  PRIMARY KEY (`product_id`),
  UNIQUE INDEX `product_id_UNIQUE` (`product_id` ASC) VISIBLE,
  INDEX `product_type_id_idx` (`product_type_id` ASC) VISIBLE,
  CONSTRAINT `product_type_id`
    FOREIGN KEY (`product_type_id`)
    REFERENCES `partners_production_company`.`product_types` (`product_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- создание таблицы запросов партнеров на продукцию
CREATE TABLE `partners_production_company`.`partner_products_requests` (
  `partner_products_request_id` INT NOT NULL AUTO_INCREMENT,
  `partner_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `product_quantity` INT NOT NULL,
  PRIMARY KEY (`partner_products_request_id`),
  UNIQUE INDEX `partner_products_request_id_UNIQUE` (`partner_products_request_id` ASC) VISIBLE,
  INDEX `partner_id_idx` (`partner_id` ASC) VISIBLE,
  INDEX `product_id_idx` (`product_id` ASC) VISIBLE,
  CONSTRAINT `partner_id`
    FOREIGN KEY (`partner_id`)
    REFERENCES `partners_production_company`.`partners` (`partner_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `product_id`
    FOREIGN KEY (`product_id`)
    REFERENCES `partners_production_company`.`products` (`product_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- Вставка типов продукции в таблицу product_types
INSERT INTO `product_types` (`name`, `coef`) VALUES
('Древесно-плитные материалы', 1.5),
('Декоративные панели', 3.5),
('Плитка', 5.25),
('Фасадные материалы', 4.5),
('Напольные покрытия', 2.17);

-- Вставка данных о продукции
INSERT INTO `products` (
  `name`,
  `articul`,
  `min_cost_for_partner`,
  `product_type_id`
) VALUES
('Фанера ФСФ 1800х1200х27 мм бежевая береза', '6549922', 5100.00,
  (SELECT product_type_id FROM product_types WHERE name = 'Древесно-плитные материалы')),
('Мягкие панели прямоугольник велюр цвет оливковый 600х300х35 мм', '7018556', 1880.00,
  (SELECT product_type_id FROM product_types WHERE name = 'Декоративные панели')),
('Бетонная плитка Белый кирпич микс 30х7,3 см', '5028272', 2080.00,
  (SELECT product_type_id FROM product_types WHERE name = 'Фасадные материалы')),
('Плитка Мозаика 10x10 см цвет белый глянец', '8028248', 2500.00,
  (SELECT product_type_id FROM product_types WHERE name = 'Плитка')),
('Ламинат Дуб Античный серый 32 класс толщина 8 мм с фаской', '9250282', 4050.00,
  (SELECT product_type_id FROM product_types WHERE name = 'Напольные покрытия')),
('Стеновая панель МДФ Флора 1440x500x10 мм', '7130981', 2100.56,
  (SELECT product_type_id FROM product_types WHERE name = 'Декоративные панели')),
('Бетонная плитка Красный кирпич 20x6,5 см', '5029784', 2760.00,
  (SELECT product_type_id FROM product_types WHERE name = 'Фасадные материалы')),
('Ламинат Канди Дизайн 33 класс толщина 8 мм с фаской', '9658953', 3200.96,
  (SELECT product_type_id FROM product_types WHERE name = 'Напольные покрытия')),
('Плита ДСП 11 мм влагостойкая 594x1815 мм', '6026662', 497.69,
  (SELECT product_type_id FROM product_types WHERE name = 'Древесно-плитные материалы')),
('Ламинат с натуральным шпоном Дуб Эксперт толщина 6 мм с фаской', '9159043', 3750.00,
  (SELECT product_type_id FROM product_types WHERE name = 'Напольные покрытия')),
('Плитка настенная Формат 20x40 см матовая цвет мята', '8588376', 2500.00,
  (SELECT product_type_id FROM product_types WHERE name = 'Плитка')),
('Плита ДСП Кантри 16 мм 900x1200 мм', '6758375', 1050.96,
  (SELECT product_type_id FROM product_types WHERE name = 'Древесно-плитные материалы')),
('Стеновая панель МДФ Сосна Полярная 60х280х4мсм цвет коричневый', '7759324', 1700.00,
  (SELECT product_type_id FROM product_types WHERE name = 'Декоративные панели')),
('Клинкерная плитка коричневая 29,8х29,8 см', '5118827', 860.00,
  (SELECT product_type_id FROM product_types WHERE name = 'Фасадные материалы')),
('Плитка настенная Цветок 60x120 см цвет зелено-голубой', '8559898', 2300.00,
  (SELECT product_type_id FROM product_types WHERE name = 'Плитка')),
('Пробковое настенное покрытие 600х300х3 мм белый', '7259474', 3300.00,
  (SELECT product_type_id FROM product_types WHERE name = 'Декоративные панели')),
('Плитка настенная Нева 30x60 см цвет серый', '8115947', 1700.00,
  (SELECT product_type_id FROM product_types WHERE name = 'Плитка')),
('Гипсовая плитка настенная Дом на берегу кирпич белый 18,5х4,5 см', '5033136', 499.00,
  (SELECT product_type_id FROM product_types WHERE name = 'Фасадные материалы')),
('Ламинат Дуб Северный белый 32 класс толщина 8 мм с фаской', '9028048', 2550.00,
  (SELECT product_type_id FROM product_types WHERE name = 'Напольные покрытия')),
('Дерево волокнистая плита Дуб Винтаж 1200х620х3 мм светло-коричневый', '6123459', 900.50,
  (SELECT product_type_id FROM product_types WHERE name = 'Древесно-плитные материалы'));

-- вставляем типы партнеров, если их еще нет
INSERT IGNORE INTO `partner_types` (`name`) VALUES
('ЗАО'), ('ООО'), ('ПАО'), ('ОАО');

-- вставляем данные партнеров
INSERT INTO `partners` (
  `name`,
  `email`,
  `phone`,
  `address`,
  `inn`,
  `rating`,
  `partner_type_id`
) VALUES
('Стройдвор', 'angelina77@kart.ru', '492 452 22 82', '143001, Московская область, город Одинцово, ул. Ленина, 21', '9432455179', 5,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ЗАО')),
('Самоделка', 'melnikov.maksim88@hm.ru', '812 267 19 59', '306230, Курская область, город Обоянь, ул. 1 Мая, 89', '7803888520', 3,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ЗАО')),
('Деревянные изделия', 'aleksejlazarev@al.ru', '922 467 93 83', '238340, Калининградская область, город Светлый, ул. Морская, 12', '8430391035', 4,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ООО')),
('Декор и отделка', 'mmsanshokova@lss.ru', '413 230 30 79', '685000, Магаданская область, город Магадан, ул. Горького, 15', '4318170454', 7,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ООО')),
('Паркет', 'ivanov.dmitrij@mail.ru', '921 851 21 22', '606440, Нижегородская область, город Бор, ул. Свободы, 3', '7687851800', 7,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ООО')),
('Дом и сад', 'ekaterina.anikeeva@ml.ru', '499 936 29 26', '393760, Тамбовская область, город Мичуринск, ул. Красная, 50', '6119144874', 7,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ПАО')),
('Легкий шаг', 'bogdanova.kseniya@bkv.ru', '495 445 61 41', '307370, Курская область, город Рыльск, ул. Гагарина, 16', '1122170258', 6,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ОАО')),
('СтройМатериалы', 'holodova@education.ru', '499 234 56 78', '140300, Московская область, город Егорьевск, ул. Советская, 24', '8355114917', 5,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ПАО')),
('Мир отделки', 'stkrylov@mail.ru', '908 713 51 88', '344116, Ростовская область, город Ростов-на-Дону, ул. Артиллерийская, 4', '3532367439', 8,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ОАО')),
('Технологии комфорта', 'kirill_belov@kir.ru', '918 432 12 34', '164500, Архангельская область, город Северодвинск, ул. Ломоносова, 29', '2362431140', 4,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ОАО')),
('Твой дом', 'dademidov@ml.ru', '919 698 75 43', '354000, Краснодарский край, город Сочи, ул. Больничная, 11', '4159215346', 10,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ПАО')),
('Новые краски', 'alievdamir@tk.ru', '812 823 93 42', '187556, Ленинградская область, город Тихвин, ул. Гоголя, 18', '9032455179', 9,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ЗАО')),
('Политехник', 'mmkotov56@educat.ru', '495 895 71 77', '143960, Московская область, город Реутов, ул. Новая, 55', '3776671267', 5,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ОАО')),
('СтройАрсенал', 'semenov.dm@mail.ru', '896 123 45 56', '242611, Брянская область, город Фокино, ул. Фокино, 23', '7447864518', 5,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ОАО')),
('Декор и порядок', 'artembolotov@ab.ru', '950 234 12 12', '309500, Белгородская область, город Старый Оскол, ул. Цветочная, 20', '9037040523', 5,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ПАО')),
('Умные решения', 'voronova_anastasiya@mail.ru', '923 233 27 69', '652050, Кемеровская область, город Юрга, ул. Мира, 42', '6221520857', 3,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ПАО')),
('Натуральные покрытия', 'vpgorbunov24@vvs.ru', '902 688 28 96', '188300, Ленинградская область, город Гатчина, пр. 25 Октября, 17', '2262431140', 9,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ЗАО')),
('СтройМастер', 'smirnov_ivan@kv.ru', '917 234 75 55', '184250, Мурманская область, город Кировск, пр. Ленина, 24', '4155215346', 9,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ООО')),
('Гранит', 'dzhumaev.ahmed@amail.ru', '495 452 55 95', '162390, Вологодская область, город Великий Устюг, ул. Железнодорожная, 36', '3961234561', 5,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ООО')),
('Строитель', 'petrov.nikolaj31@mail.ru', '916 596 15 55', '188910, Ленинградская область, город Приморск, ш. Приморское, 18', '9600275878', 10,
  (SELECT partner_type_id FROM partner_types WHERE name = 'ЗАО'));


-- вставка заявок
INSERT INTO `partner_products_requests` (
  `partner_id`,
  `product_id`,
  `product_quantity`
) VALUES
((SELECT partner_id FROM partners WHERE name = 'Стройдвор'), (SELECT product_id FROM products WHERE articul = '8028248'), 2000),
((SELECT partner_id FROM partners WHERE name = 'Самоделка'), (SELECT product_id FROM products WHERE articul = '9250282'), 3000),
((SELECT partner_id FROM partners WHERE name = 'Деревянные изделия'), (SELECT product_id FROM products WHERE articul = '6549922'), 1000),
((SELECT partner_id FROM partners WHERE name = 'Декор и отделка'), (SELECT product_id FROM products WHERE articul = '5028272'), 9500),
((SELECT partner_id FROM partners WHERE name = 'Паркет'), (SELECT product_id FROM products WHERE articul = '6549922'), 2000),
((SELECT partner_id FROM partners WHERE name = 'Дом и сад'), (SELECT product_id FROM products WHERE articul = '5033136'), 1100),
((SELECT partner_id FROM partners WHERE name = 'Легкий шаг'), (SELECT product_id FROM products WHERE articul = '6758375'), 5000),
((SELECT partner_id FROM partners WHERE name = 'СтройМатериалы'), (SELECT product_id FROM products WHERE articul = '6549922'), 2500),
((SELECT partner_id FROM partners WHERE name = 'Мир отделки'), (SELECT product_id FROM products WHERE articul = '7018556'), 6000),
((SELECT partner_id FROM partners WHERE name = 'Технологии комфорта'), (SELECT product_id FROM products WHERE articul = '7130981'), 7000),
((SELECT partner_id FROM partners WHERE name = 'Твой дом'), (SELECT product_id FROM products WHERE articul = '8028248'), 5000),
((SELECT partner_id FROM partners WHERE name = 'Новые краски'), (SELECT product_id FROM products WHERE articul = '8028248'), 7500),
((SELECT partner_id FROM partners WHERE name = 'Политехник'), (SELECT product_id FROM products WHERE articul = '6549922'), 3000),
((SELECT partner_id FROM partners WHERE name = 'СтройАрсенал'), (SELECT product_id FROM products WHERE articul = '5033136'), 500),
((SELECT partner_id FROM partners WHERE name = 'Декор и порядок'), (SELECT product_id FROM products WHERE articul = '7259474'), 7000),
((SELECT partner_id FROM partners WHERE name = 'Умные решения'), (SELECT product_id FROM products WHERE articul = '6026662'), 4000),
((SELECT partner_id FROM partners WHERE name = 'Натуральные покрытия'), (SELECT product_id FROM products WHERE articul = '6549922'), 3500),
((SELECT partner_id FROM partners WHERE name = 'СтройМастер'), (SELECT product_id FROM products WHERE articul = '6549922'), 7900),
((SELECT partner_id FROM partners WHERE name = 'Гранит'), (SELECT product_id FROM products WHERE articul = '8559898'), 9600),
((SELECT partner_id FROM partners WHERE name = 'Строитель'), (SELECT product_id FROM products WHERE articul = '8559898'), 1200),
((SELECT partner_id FROM partners WHERE name = 'Стройдвор'), (SELECT product_id FROM products WHERE articul = '8588376'), 1500),
((SELECT partner_id FROM partners WHERE name = 'Самоделка'), (SELECT product_id FROM products WHERE articul = '9658953'), 3000),
((SELECT partner_id FROM partners WHERE name = 'Деревянные изделия'), (SELECT product_id FROM products WHERE articul = '7018556'), 3010),
((SELECT partner_id FROM partners WHERE name = 'Декор и отделка'), (SELECT product_id FROM products WHERE articul = '5029784'), 3020),
((SELECT partner_id FROM partners WHERE name = 'Паркет'), (SELECT product_id FROM products WHERE articul = '9250282'), 3050),
((SELECT partner_id FROM partners WHERE name = 'Дом и сад'), (SELECT product_id FROM products WHERE articul = '5118827'), 3040),
((SELECT partner_id FROM partners WHERE name = 'Легкий шаг'), (SELECT product_id FROM products WHERE articul = '9028048'), 3050),
((SELECT partner_id FROM partners WHERE name = 'СтройМатериалы'), (SELECT product_id FROM products WHERE articul = '8028248'), 3060),
((SELECT partner_id FROM partners WHERE name = 'Мир отделки'), (SELECT product_id FROM products WHERE articul = '5033136'), 3070),
((SELECT partner_id FROM partners WHERE name = 'Технологии комфорта'), (SELECT product_id FROM products WHERE articul = '6026662'), 5400),
((SELECT partner_id FROM partners WHERE name = 'Твой дом'), (SELECT product_id FROM products WHERE articul = '6758375'), 5500),
((SELECT partner_id FROM partners WHERE name = 'Новые краски'), (SELECT product_id FROM products WHERE articul = '8588376'), 5600),
((SELECT partner_id FROM partners WHERE name = 'Политехник'), (SELECT product_id FROM products WHERE articul = '6026662'), 5700),
((SELECT partner_id FROM partners WHERE name = 'СтройАрсенал'), (SELECT product_id FROM products WHERE articul = '5118827'), 5800),
((SELECT partner_id FROM partners WHERE name = 'Декор и порядок'), (SELECT product_id FROM products WHERE articul = '7018556'), 5900),
((SELECT partner_id FROM partners WHERE name = 'Умные решения'), (SELECT product_id FROM products WHERE articul = '6758375'), 6000),
((SELECT partner_id FROM partners WHERE name = 'Натуральные покрытия'), (SELECT product_id FROM products WHERE articul = '7130981'), 6100),
((SELECT partner_id FROM partners WHERE name = 'СтройМастер'), (SELECT product_id FROM products WHERE articul = '6026662'), 8000),
((SELECT partner_id FROM partners WHERE name = 'Гранит'), (SELECT product_id FROM products WHERE articul = '5028272'), 7060),
((SELECT partner_id FROM partners WHERE name = 'Строитель'), (SELECT product_id FROM products WHERE articul = '8115947'), 6120),
((SELECT partner_id FROM partners WHERE name = 'Стройдвор'), (SELECT product_id FROM products WHERE articul = '8559898'), 5180),
((SELECT partner_id FROM partners WHERE name = 'Самоделка'), (SELECT product_id FROM products WHERE articul = '9159043'), 4240),
((SELECT partner_id FROM partners WHERE name = 'Деревянные изделия'), (SELECT product_id FROM products WHERE articul = '9159043'), 3300),
((SELECT partner_id FROM partners WHERE name = 'Декор и отделка'), (SELECT product_id FROM products WHERE articul = '9159043'), 2360),
((SELECT partner_id FROM partners WHERE name = 'Паркет'), (SELECT product_id FROM products WHERE articul = '9658953'), 1420),
((SELECT partner_id FROM partners WHERE name = 'Дом и сад'), (SELECT product_id FROM products WHERE articul = '8588376'), 1500),
((SELECT partner_id FROM partners WHERE name = 'Легкий шаг'), (SELECT product_id FROM products WHERE articul = '9250282'), 1700),
((SELECT partner_id FROM partners WHERE name = 'СтройМатериалы'), (SELECT product_id FROM products WHERE articul = '6758375'), 1900),
((SELECT partner_id FROM partners WHERE name = 'Мир отделки'), (SELECT product_id FROM products WHERE articul = '8559898'), 2100),
((SELECT partner_id FROM partners WHERE name = 'Технологии комфорта'), (SELECT product_id FROM products WHERE articul = '6758375'), 2300),
((SELECT partner_id FROM partners WHERE name = 'Твой дом'), (SELECT product_id FROM products WHERE articul = '9658953'), 2500),
((SELECT partner_id FROM partners WHERE name = 'Новые краски'), (SELECT product_id FROM products WHERE articul = '8559898'), 2700),
((SELECT partner_id FROM partners WHERE name = 'Политехник'), (SELECT product_id FROM products WHERE articul = '6758375'), 2900),
((SELECT partner_id FROM partners WHERE name = 'СтройАрсенал'), (SELECT product_id FROM products WHERE articul = '6549922'), 3100),
((SELECT partner_id FROM partners WHERE name = 'Декор и порядок'), (SELECT product_id FROM products WHERE articul = '5033136'), 3300),
((SELECT partner_id FROM partners WHERE name = 'Умные решения'), (SELECT product_id FROM products WHERE articul = '6123459'), 3500),
((SELECT partner_id FROM partners WHERE name = 'Натуральные покрытия'), (SELECT product_id FROM products WHERE articul = '9159043'), 3750),
((SELECT partner_id FROM partners WHERE name = 'СтройМастер'), (SELECT product_id FROM products WHERE articul = '5118827'), 6700),
((SELECT partner_id FROM partners WHERE name = 'Гранит'), (SELECT product_id FROM products WHERE articul = '5029784'), 6950),
((SELECT partner_id FROM partners WHERE name = 'Строитель'), (SELECT product_id FROM products WHERE articul = '8588376'), 7200),
((SELECT partner_id FROM partners WHERE name = 'Стройдвор'), (SELECT product_id FROM products WHERE articul = '8115947'), 7450),
((SELECT partner_id FROM partners WHERE name = 'Самоделка'), (SELECT product_id FROM products WHERE articul = '9028048'), 7700),
((SELECT partner_id FROM partners WHERE name = 'Деревянные изделия'), (SELECT product_id FROM products WHERE articul = '6123459'), 7950),
((SELECT partner_id FROM partners WHERE name = 'Декор и отделка'), (SELECT product_id FROM products WHERE articul = '9658953'), 8200),
((SELECT partner_id FROM partners WHERE name = 'Паркет'), (SELECT product_id FROM products WHERE articul = '9159043'), 8450),
((SELECT partner_id FROM partners WHERE name = 'Дом и сад'), (SELECT product_id FROM products WHERE articul = '5029784'), 8700),
((SELECT partner_id FROM partners WHERE name = 'Легкий шаг'), (SELECT product_id FROM products WHERE articul = '9658953'), 8950),
((SELECT partner_id FROM partners WHERE name = 'СтройМатериалы'), (SELECT product_id FROM products WHERE articul = '6123459'), 9200),
((SELECT partner_id FROM partners WHERE name = 'Мир отделки'), (SELECT product_id FROM products WHERE articul = '8028248'), 1300),
((SELECT partner_id FROM partners WHERE name = 'Технологии комфорта'), (SELECT product_id FROM products WHERE articul = '7259474'), 1500),
((SELECT partner_id FROM partners WHERE name = 'Твой дом'), (SELECT product_id FROM products WHERE articul = '7259474'), 1700),
((SELECT partner_id FROM partners WHERE name = 'Новые краски'), (SELECT product_id FROM products WHERE articul = '6758375'), 1900),
((SELECT partner_id FROM partners WHERE name = 'Политехник'), (SELECT product_id FROM products WHERE articul = '6123459'), 2100),
((SELECT partner_id FROM partners WHERE name = 'СтройАрсенал'), (SELECT product_id FROM products WHERE articul = '6026662'), 2300),
((SELECT partner_id FROM partners WHERE name = 'Декор и порядок'), (SELECT product_id FROM products WHERE articul = '7759324'), 2500),
((SELECT partner_id FROM partners WHERE name = 'Умные решения'), (SELECT product_id FROM products WHERE articul = '7759324'), 2700),
((SELECT partner_id FROM partners WHERE name = 'Натуральные покрытия'), (SELECT product_id FROM products WHERE articul = '6758375'), 2900),
((SELECT partner_id FROM partners WHERE name = 'СтройМастер'), (SELECT product_id FROM products WHERE articul = '5028272'), 3100),
((SELECT partner_id FROM partners WHERE name = 'Гранит'), (SELECT product_id FROM products WHERE articul = '5118827'), 3300),
((SELECT partner_id FROM partners WHERE name = 'Строитель'), (SELECT product_id FROM products WHERE articul = '5033136'), 3500);


ALTER TABLE `partners_production_company`.`partners`
ADD COLUMN `director_name` VARCHAR(255) NULL AFTER `name`;