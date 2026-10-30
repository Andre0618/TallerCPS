"""Cálculo del valor total a cobrar por una compra en una plataforma de comercio electrónico."""

from decimal import ROUND_HALF_UP, Decimal


class CalculadoraTarifaEnvio:
    """Calcula el total a cobrar: monto con descuentos + costo de envío."""

    ESTANDAR = "ESTANDAR"
    VIP = "VIP"
    CORPORATIVO = "CORPORATIVO"
    TIPOS_CLIENTE = frozenset({ESTANDAR, VIP, CORPORATIVO})

    DISTANCIA_MINIMA_KM = 1
    DISTANCIA_MAXIMA_KM = 500

    DESCUENTO_VIP = Decimal("0.15")
    DESCUENTO_CORPORATIVO_MENOR = Decimal("0.20")
    DESCUENTO_CORPORATIVO_MAYOR = Decimal("0.30")
    DESCUENTO_CUPON = Decimal("0.05")
    UMBRAL_CORPORATIVO = Decimal("1000.00")

    TARIFA_HASTA_50_KM = Decimal("5.00")
    TARIFA_HASTA_200_KM = Decimal("10.00")
    TARIFA_HASTA_500_KM = Decimal("20.00")
    ENVIO_GRATIS = Decimal("0.00")
    UMBRAL_ENVIO_GRATIS = Decimal("500.00")

    _CENTAVOS = Decimal("0.01")

    def calcular_total(self, monto_compra, tipo_cliente, es_cupon_valido, distancia_km):
        """Retorna el total a cobrar (monto neto + envío) como Decimal con 2 decimales.

        Lanza ValueError si monto_compra <= 0, si distancia_km está fuera de
        [1, 500] o si tipo_cliente es nulo o desconocido.
        """
        monto = self._validar_parametros(monto_compra, tipo_cliente, distancia_km)
        monto_neto = self._aplicar_descuentos(monto, tipo_cliente, es_cupon_valido)
        costo_envio = self._calcular_envio(monto, monto_neto, tipo_cliente, distancia_km)
        return monto_neto + costo_envio

    def _validar_parametros(self, monto_compra, tipo_cliente, distancia_km):
        if tipo_cliente not in self.TIPOS_CLIENTE:
            raise ValueError(f"tipo_cliente inválido: {tipo_cliente!r}")

        # Se convierte vía str para que 499.99 (float) sea exactamente Decimal("499.99").
        monto = Decimal(str(monto_compra))
        if monto <= 0:
            raise ValueError(f"monto_compra debe ser mayor a 0: {monto_compra!r}")

        if not self.DISTANCIA_MINIMA_KM <= distancia_km <= self.DISTANCIA_MAXIMA_KM:
            raise ValueError(
                f"distancia_km debe estar entre {self.DISTANCIA_MINIMA_KM} y "
                f"{self.DISTANCIA_MAXIMA_KM}: {distancia_km!r}"
            )

        return monto

    def _aplicar_descuentos(self, monto, tipo_cliente, es_cupon_valido):
        monto_neto = monto * (1 - self._descuento_por_tipo(monto, tipo_cliente))
        if es_cupon_valido:
            monto_neto *= 1 - self.DESCUENTO_CUPON
        return monto_neto.quantize(self._CENTAVOS, rounding=ROUND_HALF_UP)

    def _descuento_por_tipo(self, monto, tipo_cliente):
        if tipo_cliente == self.VIP:
            return self.DESCUENTO_VIP
        if tipo_cliente == self.CORPORATIVO:
            if monto >= self.UMBRAL_CORPORATIVO:
                return self.DESCUENTO_CORPORATIVO_MAYOR
            return self.DESCUENTO_CORPORATIVO_MENOR
        return Decimal("0")

    def _calcular_envio(self, monto, monto_neto, tipo_cliente, distancia_km):
        es_corporativo_mayor = (
            tipo_cliente == self.CORPORATIVO and monto >= self.UMBRAL_CORPORATIVO
        )
        if monto_neto >= self.UMBRAL_ENVIO_GRATIS or es_corporativo_mayor:
            return self.ENVIO_GRATIS
        if distancia_km <= 50:
            return self.TARIFA_HASTA_50_KM
        if distancia_km <= 200:
            return self.TARIFA_HASTA_200_KM
        return self.TARIFA_HASTA_500_KM
