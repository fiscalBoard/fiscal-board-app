-- phpMyAdmin SQL Dump
-- version 5.2.1deb1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 12, 2025 at 09:21 PM
-- Server version: 10.11.6-MariaDB-0+deb12u1
-- PHP Version: 8.2.24

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `NegociosDB`
--
CREATE DATABASE IF NOT EXISTS `NegociosDB` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `NegociosDB`;

-- --------------------------------------------------------

--
-- Table structure for table `Negocios`
--

CREATE TABLE `Negocios` (
  `id` int(11) NOT NULL,
  `rif` varchar(15) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `fecha_creacion` date NOT NULL,
  `tipo_negocio` enum('Comercio','Servicio','Industria','Otro') NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `password` varchar(200) NOT NULL,
  `estado` enum('Activo','Inactivo') DEFAULT 'Activo',
  PRIMARY KEY (`id`),
  UNIQUE KEY `rif` (`rif`),
  UNIQUE KEY `usuario` (`usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `AvisosSuspension`
--

CREATE TABLE `AvisosSuspension` (
  `id` int(11) NOT NULL,
  `rif` varchar(15) NOT NULL,
  `fecha_aviso` date NOT NULL,
  `motivo` varchar(255) NOT NULL,
  `fecha_reanudacion` date DEFAULT NULL,
  `ruta_imagen` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `rif` (`rif`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Carteleras`
--

CREATE TABLE `Carteleras` (
  `id` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descripcion` text NOT NULL,
  `fecha_publicacion` date NOT NULL,
  `negocio_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_negocio` (`negocio_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Documentos`
--

CREATE TABLE `Documentos` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `id_cartelera` int(11) NOT NULL,
  `tipo_documento` enum('SENIAT','IVSS','INCES','BANAVIH','MINPPST','MUNICIPAL') NOT NULL,
  `archivo` varchar(255) NOT NULL,
  `fecha_subida` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_cartelera` (`id_cartelera`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Multas`
--

CREATE TABLE `Multas` (
  `id` int(11) NOT NULL,
  `rif` varchar(15) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `fecha_emision` date NOT NULL,
  `fecha_pago` date DEFAULT NULL,
  `estado` enum('Pendiente','Pagada','Anulada') NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `ruta_imagen` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `rif` (`rif`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Propietarios`
--

CREATE TABLE `Propietarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `cedula` varchar(15) NOT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `negocio_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cedula` (`cedula`),
  KEY `negocio_id` (`negocio_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Resoluciones`
--

CREATE TABLE `Resoluciones` (
  `id` int(11) NOT NULL,
  `rif` varchar(15) NOT NULL,
  `fecha_resolucion` date NOT NULL,
  `descripcion` text NOT NULL,
  `estado` enum('Activa','Cerrada','Anulada') NOT NULL,
  `ruta_imagen` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `rif` (`rif`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Transacciones`
--

CREATE TABLE `Transacciones` (
  `id` int(11) NOT NULL,
  `negocio_id` int(11) DEFAULT NULL,
  `fecha` date NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `negocio_id` (`negocio_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Constraints for dumped tables
--

--
-- Constraints for table `AvisosSuspension`
--
ALTER TABLE `AvisosSuspension`
  ADD CONSTRAINT `AvisosSuspension_ibfk_1` FOREIGN KEY (`rif`) REFERENCES `Negocios` (`rif`);

--
-- Constraints for table `Carteleras`
--
ALTER TABLE `Carteleras`
  ADD CONSTRAINT `fk_negocio` FOREIGN KEY (`negocio_id`) REFERENCES `Negocios` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Documentos`
--
ALTER TABLE `Documentos`
  ADD CONSTRAINT `Documentos_ibfk_1` FOREIGN KEY (`id_cartelera`) REFERENCES `Carteleras` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `Multas`
--
ALTER TABLE `Multas`
  ADD CONSTRAINT `Multas_ibfk_1` FOREIGN KEY (`rif`) REFERENCES `Negocios` (`rif`);

--
-- Constraints for table `Propietarios`
--
ALTER TABLE `Propietarios`
  ADD CONSTRAINT `Propietarios_ibfk_1` FOREIGN KEY (`negocio_id`) REFERENCES `Negocios` (`id`);

--
-- Constraints for table `Resoluciones`
--
ALTER TABLE `Resoluciones`
  ADD CONSTRAINT `Resoluciones_ibfk_1` FOREIGN KEY (`rif`) REFERENCES `Negocios` (`rif`);

--
-- Constraints for table `Transacciones`
--
ALTER TABLE `Transacciones`
  ADD CONSTRAINT `Transacciones_ibfk_1` FOREIGN KEY (`negocio_id`) REFERENCES `Negocios` (`id`);

-- --------------------------------------------------------

-- Dumping data for table `Negocios`
--

INSERT INTO `Negocios` (`id`, `rif`, `nombre`, `direccion`, `telefono`, `correo`, `fecha_creacion`, `tipo_negocio`, `usuario`, `password`, `estado`) VALUES
(1, '123456', 'pepe negocio', 'Calle don Pedro', '04141824124', 'rafperezsi@gmail.com', CURDATE(), 'Comercio', 'pepeto', 'scrypt:32768:8:1$MfuJpsOuMhnfquRk$282943621d603263e0b5efb7fcec0d1d5790c7df72f6e926c264a6d84f5a6f134cf826af177e04f96d34236e0c60bb266031dd504caa5fae81629c444b467e5c', 'Activo'),
(2, 'j1343213-8', 'Industrias Gonzáles', 'Calle La Carretera, quinta La Casa . Edo Miranda', '04141689898', 'jose@email.com', CURDATE(), 'Industria', 'jose_gonzales', 'scrypt:32768:8:1$e6bE6BCi75jB0OFd$067b7ed52d84806e6a9e3d8d5f779f1a8d9b801df0432415323c0ddf109cfba6d3e28335605f1b25fb7cb3401746297d9a7be8efdb813a229061a82eadde5ba5', 'Activo'),
(11, 'j64687465', 'Servicios Juan Perez', 'Calle La Union', '04128857474', 'juan_perez@email.com', CURDATE(), 'Servicio', 'juan_perez', 'scrypt:32768:8:1$b3uFeTQsgBwYcsS3$272c71a0d76ae5607136d6763f7a1417096d6c508bffb87657df3585eb6af66ae5f0728bfc9b98e2ec6936d9805ca91dfcb24da6314d1c288d5f2a85b4a2a402', 'Activo'),
(17, '545646s', 'adadsaddsads', 'Carrrterera de la Union, Calle Don Pedro . Qta Karosales', '04123393739', 'adasdasdsa@email.com', CURDATE(), 'Industria', 'pedro_perez', 'scrypt:32768:8:1$r7fJCnMCwzlqhNDh$3fbf68c86324de2fd0bd66b2dd40463579a4e05a78cb4e5495ef0e822aa6b078560b2f68bb42f71810fe0d7427536d2e3243d9e2097e20bd4936335058fba74b', 'Activo');

-- --------------------------------------------------------

-- Dumping data for table `AvisosSuspension`
--

INSERT INTO `AvisosSuspension` (`id`, `rif`, `fecha_aviso`, `motivo`, `fecha_reanudacion`, `ruta_imagen`) VALUES
(1, '123456', '2024-10-20', 'Motivo de suspensión 1', NULL, NULL),
(2, 'j1343213-8', '2024-10-21', 'Motivo de suspensión 2', '2024-11-01', NULL);

-- --------------------------------------------------------

-- Dumping data for table `Carteleras`
--

INSERT INTO `Carteleras` (`id`, `titulo`, `descripcion`, `fecha_publicacion`, `negocio_id`) VALUES
(12, 'Cartelera 2 Propia', 'lksjad asdoa asdasdas ', CURDATE(), 2),
(14, 'Cartelera JUan', 'Mi nueva cartelera', CURDATE(), 11),
(15, 'asdasddsasda', 'adssdsadsadsadas asdsadsad', CURDATE(), 2),
(19, 'dasddsadsa', 'asdadsdasads', CURDATE(), 17),
(22, 'Mi Cartelera', 'Cartelera de prueba', CURDATE(), 1),
(23, 'Nueva cartelera ', 'kajshdksajdh asdljaskldjsa aspkojsakdljsañkdsa ', CURDATE(), 1);

-- --------------------------------------------------------

-- Dumping data for table `Documentos`
--

INSERT INTO `Documentos` (`id`, `id_cartelera`, `tipo_documento`, `archivo`, `fecha_subida`) VALUES
(10, 12, 'INCES', '/var/www/html/uploads/jose_gonzales_2_12/WhatsApp_Image_2024-10-19_at_1.29.00_PM.jpeg', '2024-10-21'),
(21, 14, 'SENIAT', '/var/www/html/uploads/juan_perez_11_14/IMG_20240905_215230_937.jpg', '2024-10-21'),
(22, 12, 'SENIAT', '/var/www/html/uploads/jose_gonzales_2_12/IMG-20241009-WA0134.jpg', '2024-10-21'),
(23, 12, 'BANAVIH', '/var/www/html/uploads/jose_gonzales_2_12/IMG-20240922-WA0012.jpg', '2024-10-21'),
(24, 12, 'MUNICIPAL', '/var/www/html/uploads/jose_gonzales_2_12/WhatsApp_Image_2024-10-02_at_2.37.08_PM_1.jpeg', '2024-10-21'),
(113, 22, 'IVSS', '/var/www/html/uploads/pepeto_1_22/INV-PAN-81932-56152-17_0.png', '2024-12-16'),
(114, 22, 'IVSS', '/var/www/html/uploads/pepeto_1_22/INV-PAN-81932-56152-17_1.png', '2024-12-16');

-- --------------------------------------------------------

-- Dumping data for table `Multas`
--

INSERT INTO `Multas` (`id`, `rif`, `monto`, `fecha_emision`, `fecha_pago`, `estado`, `descripcion`, `ruta_imagen`) VALUES
(1, '123456', 100.50, '2024-10-20', NULL, 'Pendiente', 'Descripción de multa 1', NULL),
(2, 'j1343213-8', 200.75, '2024-10-21', NULL, 'Pendiente', 'Descripción de multa 2', NULL);

-- --------------------------------------------------------

-- Dumping data for table `Propietarios`
--

INSERT INTO `Propietarios` (`id`, `nombre`, `apellido`, `cedula`, `telefono`, `correo`, `fecha_nacimiento`, `negocio_id`) VALUES
(1, 'Juan', 'Pérez', '12345678', '04120000001', 'juan.perez@email.com', '1980-05-15', 1),
(2, 'María', 'González', '87654321', '04120000002', 'maria.gonzalez@email.com', '1990-08-20', 2);

-- --------------------------------------------------------

-- Dumping data for table `Resoluciones`
--

INSERT INTO `Resoluciones` (`id`, `rif`, `fecha_resolucion`, `descripcion`, `estado`, `ruta_imagen`) VALUES
(1, '123456', '2024-10-20', 'Descripción de resolución 1', 'Activa', NULL),
(2, 'j1343213-8', '2024-10-21', 'Descripción de resolución 2', 'Activa', NULL);

-- --------------------------------------------------------

-- Dumping data for table `Transacciones`
--

INSERT INTO `Transacciones` (`id`, `negocio_id`, `fecha`, `monto`, `descripcion`) VALUES
(1, 1, '2024-10-20', 1500.00, 'Descripción de transacción 1'),
(2, 2, '2024-10-21', 2500.50, 'Descripción de transacción 2');

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;