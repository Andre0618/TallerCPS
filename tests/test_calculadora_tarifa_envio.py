"""Pruebas unitarias de CalculadoraTarifaEnvio con la estructura Arrange-Act-Assert."""

import unittest
from decimal import Decimal

from calculadora_tarifa_envio import CalculadoraTarifaEnvio


class TestCaminoFeliz(unittest.TestCase):
    """Combinaciones válidas de tipo de cliente, cupón y distancia."""

    def setUp(self):
        self.calculadora = CalculadoraTarifaEnvio()

    def test_estandar_sin_cupon_cobra_monto_completo_mas_envio(self):
        # Arrange
        monto, tipo, cupon, distancia = 100.00, "ESTANDAR", False, 10
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert
        self.assertEqual(Decimal("105.00"), total)

    def test_estandar_con_cupon_aplica_cinco_por_ciento(self):
        # Arrange
        monto, tipo, cupon, distancia = 100.00, "ESTANDAR", True, 100
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert: 100 * 0.95 = 95.00 + 10.00
        self.assertEqual(Decimal("105.00"), total)

    def test_vip_sin_cupon_aplica_quince_por_ciento(self):
        # Arrange
        monto, tipo, cupon, distancia = 200.00, "VIP", False, 300
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert: 200 * 0.85 = 170.00 + 20.00
        self.assertEqual(Decimal("190.00"), total)

    def test_vip_con_cupon_aplica_descuentos_encadenados(self):
        # Arrange
        monto, tipo, cupon, distancia = 200.00, "VIP", True, 30
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert: 200 * 0.85 * 0.95 = 161.50 + 5.00
        self.assertEqual(Decimal("166.50"), total)

    def test_corporativo_menor_a_mil_sin_cupon_aplica_veinte_por_ciento(self):
        # Arrange
        monto, tipo, cupon, distancia = 500.00, "CORPORATIVO", False, 100
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert: 500 * 0.80 = 400.00 + 10.00
        self.assertEqual(Decimal("410.00"), total)

    def test_corporativo_menor_a_mil_con_cupon_aplica_descuentos_encadenados(self):
        # Arrange
        monto, tipo, cupon, distancia = 500.00, "CORPORATIVO", True, 250
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert: 500 * 0.80 * 0.95 = 380.00 + 20.00
        self.assertEqual(Decimal("400.00"), total)

    def test_corporativo_mayor_a_mil_sin_cupon_aplica_treinta_por_ciento_y_envio_gratis(self):
        # Arrange
        monto, tipo, cupon, distancia = 2000.00, "CORPORATIVO", False, 300
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert: 2000 * 0.70 = 1400.00 + 0.00
        self.assertEqual(Decimal("1400.00"), total)

    def test_corporativo_mayor_a_mil_con_cupon_aplica_descuentos_y_envio_gratis(self):
        # Arrange
        monto, tipo, cupon, distancia = 2000.00, "CORPORATIVO", True, 300
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert: 2000 * 0.70 * 0.95 = 1330.00 + 0.00
        self.assertEqual(Decimal("1330.00"), total)

    def test_estandar_con_neto_mayor_a_quinientos_tiene_envio_gratis(self):
        # Arrange
        monto, tipo, cupon, distancia = 800.00, "ESTANDAR", False, 300
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert
        self.assertEqual(Decimal("800.00"), total)

    def test_vip_con_neto_mayor_a_quinientos_tiene_envio_gratis(self):
        # Arrange
        monto, tipo, cupon, distancia = 600.00, "VIP", False, 10
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert: 600 * 0.85 = 510.00 + 0.00
        self.assertEqual(Decimal("510.00"), total)

    def test_vip_pierde_envio_gratis_cuando_el_cupon_baja_el_neto_de_quinientos(self):
        # Arrange
        monto, tipo, cupon, distancia = 600.00, "VIP", True, 10
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert: 600 * 0.85 * 0.95 = 484.50 + 5.00
        self.assertEqual(Decimal("489.50"), total)

    def test_corporativo_menor_a_mil_con_neto_mayor_a_quinientos_tiene_envio_gratis(self):
        # Arrange
        monto, tipo, cupon, distancia = 700.00, "CORPORATIVO", False, 300
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert: 700 * 0.80 = 560.00 + 0.00
        self.assertEqual(Decimal("560.00"), total)

    def test_acepta_monto_como_decimal(self):
        # Arrange
        monto, tipo, cupon, distancia = Decimal("100.00"), "VIP", False, 10
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert: 100 * 0.85 = 85.00 + 5.00
        self.assertEqual(Decimal("90.00"), total)

    def test_total_se_retorna_como_decimal_con_dos_decimales(self):
        # Arrange
        monto, tipo, cupon, distancia = 333.33, "VIP", True, 10
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert: 333.33 * 0.85 * 0.95 = 269.164975 -> 269.16 + 5.00
        self.assertIsInstance(total, Decimal)
        self.assertEqual(-2, total.as_tuple().exponent)
        self.assertEqual(Decimal("274.16"), total)


class TestValoresLimiteMonto(unittest.TestCase):
    """Fronteras de montoCompra: 0.01, 499.99, 500.00, 999.99 y 1000.00."""

    def setUp(self):
        self.calculadora = CalculadoraTarifaEnvio()

    def test_monto_minimo_valido_cobra_monto_mas_envio(self):
        # Arrange
        monto, tipo, cupon, distancia = 0.01, "ESTANDAR", False, 10
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert
        self.assertEqual(Decimal("5.01"), total)

    def test_monto_499_99_justo_debajo_del_umbral_cobra_envio(self):
        # Arrange
        monto, tipo, cupon, distancia = 499.99, "ESTANDAR", False, 10
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert
        self.assertEqual(Decimal("504.99"), total)

    def test_monto_500_en_el_umbral_tiene_envio_gratis(self):
        # Arrange
        monto, tipo, cupon, distancia = 500.00, "ESTANDAR", False, 10
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert
        self.assertEqual(Decimal("500.00"), total)

    def test_monto_500_con_cupon_queda_bajo_el_umbral_y_cobra_envio(self):
        # Arrange
        monto, tipo, cupon, distancia = 500.00, "ESTANDAR", True, 10
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert: 500 * 0.95 = 475.00 + 5.00
        self.assertEqual(Decimal("480.00"), total)

    def test_neto_redondeado_a_500_tiene_envio_gratis(self):
        # Arrange
        monto, tipo, cupon, distancia = 526.32, "ESTANDAR", True, 10
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert: 526.32 * 0.95 = 500.004 -> 500.00 + 0.00
        self.assertEqual(Decimal("500.00"), total)

    def test_neto_redondeado_a_499_99_cobra_envio(self):
        # Arrange
        monto, tipo, cupon, distancia = 526.31, "ESTANDAR", True, 10
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert: 526.31 * 0.95 = 499.9945 -> 499.99 + 5.00
        self.assertEqual(Decimal("504.99"), total)

    def test_corporativo_999_99_aplica_veinte_por_ciento(self):
        # Arrange
        monto, tipo, cupon, distancia = 999.99, "CORPORATIVO", False, 10
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert: 999.99 * 0.80 = 799.992 -> 799.99 + 0.00
        self.assertEqual(Decimal("799.99"), total)

    def test_corporativo_1000_aplica_treinta_por_ciento(self):
        # Arrange
        monto, tipo, cupon, distancia = 1000.00, "CORPORATIVO", False, 10
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert: 1000 * 0.70 = 700.00 + 0.00
        self.assertEqual(Decimal("700.00"), total)

    def test_vip_1000_no_recibe_descuento_corporativo(self):
        # Arrange
        monto, tipo, cupon, distancia = 1000.00, "VIP", False, 10
        # Act
        total = self.calculadora.calcular_total(monto, tipo, cupon, distancia)
        # Assert: 1000 * 0.85 = 850.00 + 0.00
        self.assertEqual(Decimal("850.00"), total)


class TestValoresLimiteDistancia(unittest.TestCase):
    """Fronteras de distanciaKm: 1, 50, 51, 200, 201 y 500 (neto de 100.00, sin envío gratis)."""

    def setUp(self):
        self.calculadora = CalculadoraTarifaEnvio()
        self.monto = 100.00
        self.tipo = "ESTANDAR"
        self.cupon = False

    def test_distancia_1_cobra_tarifa_de_5(self):
        # Arrange
        distancia = 1
        # Act
        total = self.calculadora.calcular_total(self.monto, self.tipo, self.cupon, distancia)
        # Assert
        self.assertEqual(Decimal("105.00"), total)

    def test_distancia_50_cobra_tarifa_de_5(self):
        # Arrange
        distancia = 50
        # Act
        total = self.calculadora.calcular_total(self.monto, self.tipo, self.cupon, distancia)
        # Assert
        self.assertEqual(Decimal("105.00"), total)

    def test_distancia_51_cobra_tarifa_de_10(self):
        # Arrange
        distancia = 51
        # Act
        total = self.calculadora.calcular_total(self.monto, self.tipo, self.cupon, distancia)
        # Assert
        self.assertEqual(Decimal("110.00"), total)

    def test_distancia_200_cobra_tarifa_de_10(self):
        # Arrange
        distancia = 200
        # Act
        total = self.calculadora.calcular_total(self.monto, self.tipo, self.cupon, distancia)
        # Assert
        self.assertEqual(Decimal("110.00"), total)

    def test_distancia_201_cobra_tarifa_de_20(self):
        # Arrange
        distancia = 201
        # Act
        total = self.calculadora.calcular_total(self.monto, self.tipo, self.cupon, distancia)
        # Assert
        self.assertEqual(Decimal("120.00"), total)

    def test_distancia_500_cobra_tarifa_de_20(self):
        # Arrange
        distancia = 500
        # Act
        total = self.calculadora.calcular_total(self.monto, self.tipo, self.cupon, distancia)
        # Assert
        self.assertEqual(Decimal("120.00"), total)


class TestExcepciones(unittest.TestCase):
    """Entradas inválidas que deben lanzar ValueError."""

    def setUp(self):
        self.calculadora = CalculadoraTarifaEnvio()

    def test_monto_cero_lanza_value_error(self):
        # Arrange
        monto, tipo, cupon, distancia = 0, "ESTANDAR", False, 10
        # Act / Assert
        with self.assertRaisesRegex(ValueError, "monto_compra"):
            self.calculadora.calcular_total(monto, tipo, cupon, distancia)

    def test_monto_negativo_minimo_lanza_value_error(self):
        # Arrange
        monto, tipo, cupon, distancia = -0.01, "ESTANDAR", False, 10
        # Act / Assert
        with self.assertRaisesRegex(ValueError, "monto_compra"):
            self.calculadora.calcular_total(monto, tipo, cupon, distancia)

    def test_monto_negativo_lanza_value_error(self):
        # Arrange
        monto, tipo, cupon, distancia = -100.00, "VIP", True, 10
        # Act / Assert
        with self.assertRaisesRegex(ValueError, "monto_compra"):
            self.calculadora.calcular_total(monto, tipo, cupon, distancia)

    def test_distancia_cero_lanza_value_error(self):
        # Arrange
        monto, tipo, cupon, distancia = 100.00, "ESTANDAR", False, 0
        # Act / Assert
        with self.assertRaisesRegex(ValueError, "distancia_km"):
            self.calculadora.calcular_total(monto, tipo, cupon, distancia)

    def test_distancia_negativa_lanza_value_error(self):
        # Arrange
        monto, tipo, cupon, distancia = 100.00, "ESTANDAR", False, -5
        # Act / Assert
        with self.assertRaisesRegex(ValueError, "distancia_km"):
            self.calculadora.calcular_total(monto, tipo, cupon, distancia)

    def test_distancia_501_lanza_value_error(self):
        # Arrange
        monto, tipo, cupon, distancia = 100.00, "ESTANDAR", False, 501
        # Act / Assert
        with self.assertRaisesRegex(ValueError, "distancia_km"):
            self.calculadora.calcular_total(monto, tipo, cupon, distancia)

    def test_tipo_cliente_nulo_lanza_value_error(self):
        # Arrange
        monto, tipo, cupon, distancia = 100.00, None, False, 10
        # Act / Assert
        with self.assertRaisesRegex(ValueError, "tipo_cliente"):
            self.calculadora.calcular_total(monto, tipo, cupon, distancia)

    def test_tipo_cliente_desconocido_lanza_value_error(self):
        # Arrange
        monto, tipo, cupon, distancia = 100.00, "PREMIUM", False, 10
        # Act / Assert
        with self.assertRaisesRegex(ValueError, "tipo_cliente"):
            self.calculadora.calcular_total(monto, tipo, cupon, distancia)

    def test_tipo_cliente_en_minusculas_lanza_value_error(self):
        # Arrange
        monto, tipo, cupon, distancia = 100.00, "vip", False, 10
        # Act / Assert
        with self.assertRaisesRegex(ValueError, "tipo_cliente"):
            self.calculadora.calcular_total(monto, tipo, cupon, distancia)

    def test_tipo_cliente_vacio_lanza_value_error(self):
        # Arrange
        monto, tipo, cupon, distancia = 100.00, "", False, 10
        # Act / Assert
        with self.assertRaisesRegex(ValueError, "tipo_cliente"):
            self.calculadora.calcular_total(monto, tipo, cupon, distancia)


if __name__ == "__main__":
    unittest.main()
