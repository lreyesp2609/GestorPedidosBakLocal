CREATE TABLE Cuenta (
    id_Cuenta SERIAL PRIMARY KEY,
    NombreUsuario VARCHAR(300) NOT null UNIQUE ,
    Contrasenia VARCHAR NOT NULL,
    FechaCreacion TIMESTAMP NOT NULL,
    FechaFin TIMESTAMP,
    Observacion VARCHAR(500),
    FotoPerfil BYTEA, 
    EstadoCuenta CHAR(1) CHECK (EstadoCuenta IN ('0', '1')) NOT NULL,
    Rol CHAR(1) CHECK (Rol IN ('A', 'C', 'X', 'M', 'D','S')) NOT NULL,
    CorreoRecuperacion VARCHAR(256)
);
CREATE TABLE Empresa (
    id_Empresa SERIAL PRIMARY KEY,
    ENombre VARCHAR(200) NOT NULL,
    Direccion VARCHAR(300),
    Etelefono VARCHAR(10),
    CorreoElectronico VARCHAR(256),
    FechaFundacion DATE NOT NULL,
    SitioWeb VARCHAR(2000),
    Eslogan VARCHAR(300),
    Elogo BYTEA,
    EDescripcion VARCHAR(800),
    DocMenu BYTEA
);
CREATE TABLE Ubicaciones (
    id_Ubicacion SERIAL PRIMARY KEY,
    Latitud DECIMAL(9,6) NOT NULL,
    Longitud DECIMAL(9,6) NOT NULL,
    UDescripcion VARCHAR(500),
	SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);
CREATE TABLE GeoSectores (
    id_Geosector SERIAL PRIMARY KEY,
    FechaCreacionG TIMESTAMP NOT NULL,
    SecNombre VARCHAR(300) NOT NULL,
    SecDescripcion VARCHAR(500),
    SecTipo CHAR(1) CHECK (SecTipo IN ('C', 'R', 'T')) NOT NULL,
    SecEstado CHAR(1) CHECK (SecEstado IN ('0', '1')) NOT NULL,
    Tarifa NUMERIC(10,2),
	SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);
CREATE TABLE HorariosSemanales (
    id_HorarioS SERIAL PRIMARY KEY,
    HorDescripcion VARCHAR(500),
    TipoHorario CHAR(1) CHECK (TipoHorario IN ('P', 'C', 'X', 'A')) NOT NULL,
    NombreH VARCHAR(200) NOT NULL
);
CREATE TABLE DetalleHorariosSemanales (
    id_DetHorarioS SERIAL PRIMARY KEY,
    id_HorarioS INTEGER REFERENCES HorariosSemanales(id_HorarioS) NOT NULL,
    Dia CHAR(1) CHECK (Dia IN ('L', 'M', 'X', 'J', 'V', 'S', 'D')) NOT NULL,
    HoraInicio TIME NOT NULL,
    HoraFin TIME NOT NULL
);
CREATE TABLE AvisosPrincipales (
    id_Aviso SERIAL PRIMARY KEY,
    id_Empresa INTEGER REFERENCES Empresa(id_Empresa) NOT NULL,
    Titulo VARCHAR(150) NOT NULL,
    Descripcion VARCHAR(500),
    Imagen BYTEA NOT NULL,
	SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);
CREATE TABLE Redes (
    id_Red SERIAL PRIMARY KEY,
    id_Empresa INTEGER REFERENCES Empresa(id_Empresa) NOT NULL,
    Nombre VARCHAR(50) NOT NULL,
    url VARCHAR(2000) NOT NULL,
    RLogo BYTEA NOT NULL
);

CREATE TABLE Sucursales (
    id_Sucursal SERIAL PRIMARY KEY,
    SRazon_social VARCHAR(300) NOT NULL,
    SRUC VARCHAR(20) NOT NULL,
    SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL,
    SCapacidad CHAR(1) CHECK (SCapacidad IN ('P', 'S')),
    SCorreo VARCHAR(300) NOT NULL,
    STelefono VARCHAR(300),
    SDireccion VARCHAR(300) NOT NULL,
    SNombre VARCHAR(300),
    FSApertura DATE,
    id_HorarioS INTEGER REFERENCES HorariosSemanales(id_HorarioS),
    id_GeoSector INTEGER REFERENCES GeoSectores(id_GeoSector),
    FirmaElectronica BYTEA,
    id_Empresa INTEGER REFERENCES Empresa(id_Empresa) NOT NULL,
    id_Ubicacion INTEGER REFERENCES Ubicaciones(id_Ubicacion),
    ImagenSucursal BYTEA,
	id_Cuenta INTEGER REFERENCES cuenta(id_Cuenta)
);

CREATE TABLE UnidadMedida (
    idUM SERIAL PRIMARY KEY,
    nombreUM VARCHAR(100) NOT NULL,
	SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);
CREATE TABLE EnsambleUnidadMedida (
    idEUM SERIAL PRIMARY KEY,
    idUMP INTEGER REFERENCES UnidadMedida(idUM),
	idUMc INTEGER REFERENCES UnidadMedida(idUM),
	CantidadConversion NUMERIC(12,6) NOT NULL
);


CREATE TABLE TiposProductos (
    id_Tipoproducto SERIAL PRIMARY KEY,
    TPNombre VARCHAR(300) NOT NULL,
    Descripcion VARCHAR(500),
	SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);
CREATE TABLE Categorias (
    id_Categoria SERIAL PRIMARY KEY,
    ImagenCategoria BYTEA, 
    id_Tipoproducto INTEGER REFERENCES TiposProductos(id_Tipoproducto) NOT NULL,
    CatNombre VARCHAR(300) NOT NULL,
    Descripcion VARCHAR(500),
	SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);
CREATE TABLE Componente (
    id_Componente SERIAL PRIMARY KEY,
    Nombre VARCHAR(300) NOT NULL,
	id_Categoria INTEGER REFERENCES Categorias(id_Categoria)NOT NULL,
    Descripcion VARCHAR(500),
    Costo MONEY,
    Tipo CHAR(1) CHECK (Tipo IN ('N', 'F')) NOT NULL,
    id_UM INTEGER REFERENCES UnidadMedida(idUM) NOT NULL,
	SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);

CREATE TABLE EnsambleComponente (
    id_ensambleC SERIAL PRIMARY KEY,
    id_componentePadre INTEGER REFERENCES Componente(id_Componente)NOT NULL,
    PadreCantidad NUMERIC(9,2) NOT NULL,
    id_UmPadre INTEGER REFERENCES UnidadMedida(idUM) NOT NULL
);
CREATE TABLE DetalleEnsambleComponente (
    id_DetalleEnsambleC SERIAL PRIMARY KEY,
    id_ensambleC INTEGER REFERENCES EnsambleComponente(id_ensambleC) NOT NULL,
    id_componenteHijo INTEGER REFERENCES Componente(id_Componente)NOT NULL,
    CantidadHijo NUMERIC(9,2) NOT NULL,
    id_UmHijo INTEGER REFERENCES UnidadMedida(idUM) NOT NULL
);
CREATE TABLE Producto (
    id_Producto SERIAL PRIMARY KEY,
    id_Categoria INTEGER REFERENCES Categorias(id_Categoria)NOT NULL,
    id_UM INTEGER REFERENCES UnidadMedida(idUM) NOT NULL,
    ImagenP BYTEA,
    PuntosP NUMERIC(3) NOT NULL,
    CodPrincipal VARCHAR(25) NOT NULL,
    NombreProducto VARCHAR(300) NOT NULL unique,
    DescripcionProducto VARCHAR(300),
    PrecioUnitario NUMERIC(14,2) NOT NULL,
    IVA CHAR(1) CHECK (IVA IN ('0', '1')) NOT NULL,
    ICE CHAR(1) CHECK (ICE IN ('0', '1')) NOT NULL,
    IRBPNR CHAR(1) CHECK (IRBPNR IN ('0', '1')) NOT NULL,
	SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);


CREATE TABLE EnsambleProducto (
    id_emsambleP SERIAL PRIMARY KEY,
    id_Producto INTEGER REFERENCES Producto(id_Producto) NOT NULL,
    PadreCantidad NUMERIC(9,2) NOT NULL,
    id_Um INTEGER REFERENCES UnidadMedida(idUM) NOT NULL
);

CREATE TABLE DetalleEnsambleProducto (
    id_DetalleEnsambleP SERIAL PRIMARY KEY,
    id_emsambleP INTEGER REFERENCES EnsambleProducto(id_emsambleP) NOT NULL,
    id_componenteHijo INTEGER REFERENCES Componente(id_Componente) NOT NULL,
    CantidadHijo NUMERIC(9,2) NOT NULL,
    id_UmHijo INTEGER REFERENCES UnidadMedida(idUM) NOT NULL
);
CREATE TABLE CategoriasCombos (
    id_CatCombo SERIAL PRIMARY KEY,
    ImagenCategoria BYTEA, 
    CatNombre VARCHAR(300) NOT NULL unique,
    Descripcion VARCHAR(500),
	SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);
CREATE TABLE Combo (
    id_Combo SERIAL PRIMARY KEY,
    id_CatCombo INTEGER REFERENCES CategoriasCombos(id_CatCombo) NOT NULL,
    ImagenC BYTEA, 
    PuntosCb NUMERIC(3),
    CodPrincipal VARCHAR(25) NOT NULL,
    NombreCb VARCHAR(300),
    DescripcionCombo VARCHAR(300),
    PrecioUnitario NUMERIC(14,2) NOT NULL,
    IVA CHAR(1) CHECK (IVA IN ('0', '1')) NOT NULL,
    ICE CHAR(1) CHECK (ICE IN ('0', '1')) NOT NULL,
    IRBPNR CHAR(1) CHECK (IRBPNR IN ('0', '1')) NOT NULL,
	SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);

CREATE TABLE DetalleCombo (
    id_DetalleCombo SERIAL PRIMARY KEY,
    id_Combo INTEGER REFERENCES Combo(id_Combo) NOT NULL,
    id_Producto INTEGER REFERENCES Producto(id_Producto) NOT NULL,
    Cantidad INTEGER
);

CREATE TABLE Clientes (
    id_Cliente SERIAL PRIMARY KEY,
    CRazon_Social VARCHAR(300) ,
    CTelefono VARCHAR(300) NOT NULL UNIQUE,
    TipoCliente VARCHAR(2) CHECK (TipoCliente IN ('04', '05', '06', '07', '08')),
    CRegistro TIMESTAMP NOT NULL,
    SNombre VARCHAR(300),
    CApellido VARCHAR(300),
    CPuntos NUMERIC(3) NOT NULL,
    id_Ubicacion1 INTEGER REFERENCES Ubicaciones(id_Ubicacion),
    id_Ubicacion2 INTEGER REFERENCES Ubicaciones(id_Ubicacion),
    id_Ubicacion3 INTEGER REFERENCES Ubicaciones(id_Ubicacion),
	id_Cuenta INTEGER REFERENCES cuenta(id_Cuenta),
    RUC_Cedula VARCHAR(300) UNIQUE,
    CCorreo_Electronico VARCHAR(300),
    Ubicacion VARCHAR(300),
	SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);
CREATE TABLE Administrador (
    id_Administrador SERIAL PRIMARY KEY,
    Telefono CHAR(10),
    Apellido VARCHAR(300) NOT NULL,
    Nombre VARCHAR(300) NOT NULL,
    id_Cuenta INTEGER REFERENCES Cuenta(id_Cuenta) NOT NULL,
    id_Sucursal INTEGER REFERENCES Sucursales(id_Sucursal)
);

CREATE TABLE Mesas (
    id_Mesa SERIAL PRIMARY KEY,
    id_Administrador INTEGER REFERENCES Administrador(id_Administrador) NOT NULL,
    Observacion VARCHAR(500),
    Estado CHAR(1) CHECK (Estado IN ('D', 'R', 'U', 'A')) NOT NULL,
    Activa CHAR(1) CHECK (Activa IN ('0', '1')) NOT NULL,
    MaxPersonas SMALLINT NOT NULL,
	SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);
CREATE TABLE Motorizados (
	id_Motorizado SERIAL PRIMARY KEY, 
	id_Sucursal INTEGER REFERENCES Sucursales(id_Sucursal) NOT NULL,
	id_Administrador INTEGER REFERENCES Administrador(id_Administrador) NOT NULL,
	Nombre VARCHAR(300) NOT NULL,
	Apellido VARCHAR(300)NOT NULL,
	Telefono VARCHAR(10),
	Fecha_registro TIMESTAMP NOT NULL,
	id_Cuenta INTEGER REFERENCES cuenta(id_Cuenta),
	SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);

CREATE TABLE jefecocina (
	id_jefecocina SERIAL PRIMARY KEY, 
	id_Sucursal INTEGER REFERENCES Sucursales(id_Sucursal) NOT NULL,
	id_Administrador INTEGER REFERENCES Administrador(id_Administrador) NOT NULL,
	Nombre VARCHAR(300) NOT NULL,
	Apellido VARCHAR(300)NOT NULL,
	Telefono VARCHAR(10),
	Fecha_registro TIMESTAMP NOT NULL,
	id_Cuenta INTEGER REFERENCES cuenta(id_Cuenta),
	SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);

CREATE TABLE RutasProgramadas (
	id_RutaProgramada SERIAL PRIMARY KEY,
	id_Motorizado INTEGER REFERENCES Motorizados(id_Motorizado) NOT NULL,
	id_Administrador INTEGER REFERENCES Administrador(id_Administrador) NOT NULL,
	id_Geosector INTEGER REFERENCES GeoSectores(id_Geosector) NOT NULL,
	Fecha_inicio DATE,
	Fecha_fin DATE
);

CREATE TABLE Promociones (
	id_Promocion SERIAL PRIMARY KEY,
	id_Combo INTEGER REFERENCES Combo(id_Combo) NOT NULL,
	nombrePromocion VARCHAR(300),
	SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);

CREATE TABLE Pedidos (
	id_Pedido SERIAL PRIMARY KEY,
	id_Cliente INTEGER REFERENCES Clientes(id_Cliente) NOT NULL,
	Precio NUMERIC(10, 2) NOT NULL,
	Tipo_de_pedido CHAR(1) CHECK (Tipo_de_pedido IN ('D', 'R', 'L')) NOT NULL,
	Metodo_de_pago CHAR(1) CHECK (Metodo_de_pago IN ('E', 'T', 'X', 'F')) NOT NULL,
	Puntos NUMERIC(3) NOT NULL,
	Fecha_pedido TIMESTAMP NOT NULL,
	Fecha_entrega TIMESTAMP,
	Estado_del_pedido CHAR NOT NULL CHECK (Estado_del_pedido IN ('O', 'P', 'C', 'E','R')) NOT NULL,
	Observacion_del_cliente VARCHAR(500),
    imagen BYTEA,
    estado_pago varchar(100),
	id_Ubicacion INTEGER REFERENCES Ubicaciones(id_Ubicacion),
	id_Sucursal INTEGER REFERENCES Sucursales(id_Sucursal)
);
 
CREATE TABLE DetallePedidos (
	id_detallePedido SERIAL PRIMARY KEY,
	id_Pedido INTEGER REFERENCES Pedidos(id_Pedido) NOT NULL,
	id_Producto INTEGER REFERENCES Producto(id_Producto),
	id_Combo INTEGER REFERENCES Combo(id_Combo),
	id_Promocion INTEGER REFERENCES Promociones(id_Promocion),
	Cantidad NUMERIC NOT NULL,
	Precio_unitario NUMERIC(9,2),
	Impuesto NUMERIC(9,2),
	Descuento NUMERIC(9,2)
);


CREATE TABLE Bodegas (
	id_Bodega SERIAL PRIMARY KEY,
	nombreBog VARCHAR(300) NOT NULL,
	Descripcion VARCHAR(500),
	id_Sucursal INTEGER REFERENCES Sucursales(Id_Sucursal) NOT NULL,
	SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);

CREATE TABLE Inventario (
    id_Inventario SERIAL PRIMARY KEY,
    id_Bodega INTEGER REFERENCES Bodegas(id_Bodega) NOT NULL,
    id_Producto INTEGER REFERENCES Producto(id_Producto),
    id_Componente INTEGER REFERENCES Componente(id_Componente),
    Costo_unitario NUMERIC(9,2),
    id_UM INTEGER REFERENCES UnidadMedida(idUM),
    Stock_minimo DECIMAL(9,2),
    Cantidad_disponible DECIMAL(9,2) NOT NULL CHECK (Cantidad_disponible >= 0)
);

CREATE TABLE Procesamiento (
	id_Procesamientos SERIAL PRIMARY KEY,
	id_Cuenta INTEGER REFERENCES Cuenta(id_Cuenta) NOT NULL,
	Tipo_de_proceso CHAR(1) check (Tipo_de_proceso IN ('V', 'C', 'I', 'R', 'E')) NOT NULL,
	Observacion VARCHAR(500),
	Fecha_de_procesamiento TIMESTAMP NOT NULL,	
	id_Bodega INTEGER REFERENCES Bodegas(id_Bodega ) NOT NULL
);

CREATE TABLE DetalleProcesamiento (
	id_DetalleP SERIAL PRIMARY KEY,
	id_Procesamientos INTEGER REFERENCES Procesamiento(id_Procesamientos) NOT NULL,
	id_Inventario INTEGER REFERENCES Inventario(id_Inventario) NOT NULL,
	Cantidad DECIMAL(9,2) NOT NULL,
	id_Pedido INTEGER REFERENCES Pedidos(id_Pedido),
	id_InventarioGenerado INTEGER REFERENCES Inventario(id_Inventario)
);

CREATE TABLE Casillero (
	id_Casillero SERIAL PRIMARY KEY,
	id_Motorizado INTEGER REFERENCES Motorizados(id_Motorizado),
	Descripcion VARCHAR(500),
	Nombre VARCHAR (300) NOT NULL,
	Fecha_creacion TIMESTAMP NOT NULL,
	id_Sucursal INTEGER REFERENCES Sucursales(Id_Sucursal) NOT NULL,
	id_Administrador INTEGER REFERENCES Administrador(id_Administrador) NOT NULL,
	Cantidad_actual NUMERIC(9,2) NOT NULL,
	Caja CHAR(1) check (Caja IN ('1', '0')) NOT NULL,
	SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);

CREATE TABLE MovimientosCasilleros (
	id_Movimiento SERIAL PRIMARY KEY,
	tipoMovimiento CHAR(1) check (tipoMovimiento IN ('E', 'S')) NOT NULL,
	id_Casillero INTEGER REFERENCES Casillero(id_Casillero) NOT NULL,
	Cantidad NUMERIC(9,2) NOT NULL,
	id_Cuenta INTEGER REFERENCES Cuenta(id_Cuenta) NOT NULL,
	Observacion VARCHAR(500),
	id_CasilleroS INTEGER REFERENCES Casillero(id_Casillero)
);

CREATE TABLE HorariosProductosSemana (
	id_HorxProducto SERIAL PRIMARY KEY, 
	id_Producto INTEGER REFERENCES Producto(id_Producto) NOT NULL,
	id_HorarioS INTEGER REFERENCES HorariosProductosSemana(id_HorxProducto) NOT NULL
);

CREATE TABLE Reservaciones (
    id_Reservacion SERIAL PRIMARY KEY,
    id_Cliente INTEGER REFERENCES Clientes(id_Cliente) NOT NULL,
    id_Mesa INTEGER REFERENCES Mesas(id_Mesa) NOT NULL,
    Fecha_reserva DATE NOT NULL,
    Hora_reserva TIME NOT NULL,    
	Estado CHAR(1) check (Estado IN ('E', 'D', 'F')) NOT NULL
);

CREATE TABLE meseros (
	id_Mesero SERIAL PRIMARY KEY,
	id_Sucursal INTEGER REFERENCES Sucursales(id_Sucursal) NOT NULL,
	id_Administrador INTEGER REFERENCES Administrador(id_Administrador) NOT NULL,
	Telefono VARCHAR(10) NOT NULL,
	Apellido VARCHAR(300) NOT NULL,
	Nombre VARCHAR(300) NOT NULL,
	Fecha_registro TIMESTAMP NOT NULL,
	id_Cuenta INTEGER REFERENCES cuenta(id_Cuenta),
	SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);

CREATE TABLE PedidosMesa (
	id_PMesa SERIAL PRIMARY KEY, 
	id_Mesero INTEGER REFERENCES meseros(id_Mesero) NOT NULL,
	id_Mesa INTEGER REFERENCES Mesas(id_Mesa) NOT NULL,
	id_Pedido INTEGER REFERENCES Pedidos(id_Pedido) NOT NULL
);

CREATE TABLE Envios (
	id_Envio SERIAL PRIMARY KEY,
	Fecha_de_envio TIMESTAMP NOT NULL,
	Estado CHAR(1) check (Estado IN ('T', 'C')) NOT NULL,	
	Fecha_de_entrega TIMESTAMP,
	id_Motorizado INTEGER REFERENCES Motorizados(id_Motorizado) NOT NULL
);

CREATE TABLE PagosEfectivo (
	id_pagoEfectivo SERIAL PRIMARY KEY, 
	Estado CHAR(1) check (Estado IN ('X', 'P')) NOT NULL,
	Cantidad NUMERIC(9,2) NOT NULL, 
	CantidadEntregada NUMERIC(9,2) NOT NULL,
	CambioeEntregado NUMERIC(9,2) NOT NULL,
	Hora_de_pago TIMESTAMP NOT NULL,
	id_cuentaCobrador INTEGER REFERENCES Cuenta(id_Cuenta) NOT NULL,
	id_Pedido INTEGER REFERENCES Pedidos(id_Pedido) NOT NULL
);

CREATE TABLE PagosTransferencia (
	id_pagoTransferencia SERIAL PRIMARY KEY, 
	id_Pedido INTEGER REFERENCES Pedidos(id_Pedido) NOT NULL,
	Estado CHAR(1) check (Estado IN ('E', 'C')) NOT NULL,
	Cantidad NUMERIC(9,2) NOT NULL,
	Hora_de_pago TIMESTAMP NOT NULL,
	id_cuentaCobrador INTEGER REFERENCES Cuenta(id_Cuenta),
	Comprobante BYTEA NOT NULL,
	Hora_confirmacion_pago TIMESTAMP
);

CREATE TABLE PagosPasarela (
	id_pagoPasarela SERIAL PRIMARY KEY,
	id_Pedido INTEGER REFERENCES Pedidos(id_Pedido) NOT NULL,
	Estado CHAR(1) check (Estado IN ('E', 'C')) NOT NULL,
	Cantidad NUMERIC(9,2) NOT NULL,
	Hora_de_pago TIMESTAMP NOT NULL,
	Codigo_unico INTEGER
);

CREATE TABLE PagosFraccionados (
	id_pagoFraccionado SERIAL PRIMARY KEY,
	id_pagoEfectivo INTEGER REFERENCES PagosEfectivo(id_pagoEfectivo) NOT NULL,
	id_pagoTransferencia INTEGER REFERENCES PagosTransferencia(id_pagoTransferencia) NOT NULL,
	id_pagoPasarela INTEGER REFERENCES PagosPasarela(id_pagoPasarela) NOT NULL,
	Cantidad NUMERIC(9,2) NOT NULL,
	Hora_de_pago INTEGER
);

CREATE TABLE Proveedores (
    id_Proveedor SERIAL PRIMARY KEY,
    NombreProveedor VARCHAR(300) NOT NULL,
    DireccionProveedor VARCHAR(300),
    TelefonoProveedor VARCHAR(10),
    CorreoProveedor VARCHAR(256),
    id_Administrador INTEGER REFERENCES Administrador(id_Administrador),
    SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);

CREATE TABLE Compras (
    id_Compra SERIAL PRIMARY KEY,
    id_Proveedor INTEGER REFERENCES Proveedores(id_Proveedor) NOT NULL,
    id_Administrador INTEGER REFERENCES Administrador(id_Administrador) NOT NULL,
    FechaCompra TIMESTAMP NOT NULL,
    id_Procesamiento INTEGER REFERENCES Procesamiento(id_Procesamientos) NOT NULL
);

CREATE TABLE DetalleCompra (
    id_DetalleCompra SERIAL PRIMARY KEY,
    id_Compra INTEGER REFERENCES Compras(id_Compra) NOT NULL,
    id_Producto INTEGER REFERENCES Producto(id_Producto),
    id_Componente INTEGER REFERENCES Componente(id_Componente),
    Cantidad NUMERIC(9,2) NOT NULL,
    Precio NUMERIC(9,2) NOT NULL,
    id_UM INTEGER REFERENCES UnidadMedida(idUM) NOT NULL
);
CREATE TABLE horarioproducto (
    id_HorarioProducto SERIAL PRIMARY KEY,
    id_HorarioS INTEGER REFERENCES HorariosSemanales(id_HorarioS) NOT NULL,
    id_Sucursal INTEGER REFERENCES Sucursales(id_Sucursal) NOT NULL,
    id_Producto INTEGER REFERENCES Producto(id_Producto) NOT NULL
);
CREATE TABLE RecompensasProductos (
    id_RecompensaProducto SERIAL PRIMARY KEY,
    id_Producto INTEGER REFERENCES Producto(id_Producto) NOT NULL,
    Puntos_Recompensa_Producto NUMERIC(3) NOT NULL,
    SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL,
    CONSTRAINT chk_puntos CHECK (Puntos_Recompensa_Producto >= 0),
    CONSTRAINT uk_id_Producto UNIQUE (id_Producto)  -- Restricción de unicidad
);

CREATE TABLE RecompensasCombos (
    id_RecompensaCombo SERIAL PRIMARY KEY,
    id_Combo INTEGER REFERENCES Combo(id_Combo) NOT NULL,
    Puntos_Recompensa_Combo NUMERIC(3) NOT NULL,
    SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL,
    CONSTRAINT chk_puntos CHECK (Puntos_Recompensa_Combo >= 0),
    CONSTRAINT uk_id_Combo UNIQUE (id_Combo)  -- Restricción de unicidad
);
CREATE TABLE detalle_geosector (
    id_detallegeosector SERIAL PRIMARY KEY,
    id_geosector INTEGER REFERENCES geosectores(id_geosector),
    id_ubicacion INTEGER REFERENCES ubicaciones(id_ubicacion)
);
CREATE TABLE pedidosproveedor
(
    id_pedidoproveedor SERIAL PRIMARY KEY,
    id_proveedor INTEGER REFERENCES public.proveedores(id_proveedor) NOT NULL,
    id_bodega INTEGER REFERENCES public.bodegas(id_bodega) NOT NULL,
    fechapedido TIMESTAMP NOT NULL,
    fechaentregaesperada TIMESTAMP,
    estado CHAR(1) NOT NULL,
    observacion VARCHAR(500),
    CONSTRAINT fk_pedidosproveedor_proveedores FOREIGN KEY (id_proveedor) REFERENCES public.proveedores(id_proveedor),
    CONSTRAINT fk_pedidosproveedor_bodegas FOREIGN KEY (id_bodega) REFERENCES public.bodegas(id_bodega)
);

CREATE TABLE detallepedidoproveedor
(
    id_detallepedidoproveedor SERIAL PRIMARY KEY,
    id_pedidoproveedor INTEGER REFERENCES pedidosproveedor(id_pedidoproveedor) NOT NULL,
    id_producto INTEGER REFERENCES producto(id_producto),
    id_componente INTEGER REFERENCES componente(id_componente),
    cantidad NUMERIC(9,2) NOT NULL,
    costounitario NUMERIC(9,2) NOT NULL,
    id_um INTEGER REFERENCES unidadmedida(idum) NOT NULL
);

CREATE TABLE PuntoFacturacion (
    id_PuntoFacturacion SERIAL PRIMARY KEY,
    NombrePunto VARCHAR(100) NOT NULL,
    id_Mesero INTEGER REFERENCES Meseros(id_Mesero),
    id_administrador INTEGER REFERENCES administrador(id_administrador),
    Codigo VARCHAR(3) NOT NULL,
    RUC VARCHAR(13),
    SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);

CREATE TABLE Factura (
    id_factura SERIAL PRIMARY KEY,
    id_pedido INTEGER REFERENCES Pedidos(id_pedido),
    id_cliente INTEGER REFERENCES Clientes(id_cliente),
    id_mesero INTEGER REFERENCES Meseros(id_mesero),
    id_punto_facturacion INTEGER REFERENCES PuntoFacturacion(id_PuntoFacturacion),
    fecha_emision TIMESTAMP,
    total NUMERIC(10, 2),
    iva NUMERIC(10, 2),
    descuento NUMERIC(10, 2),
    subtotal NUMERIC(10, 2),
    a_pagar NUMERIC(10, 2),
    codigo_factura VARCHAR(15),
    codigo_autorizacion VARCHAR(49),
    numero_factura_desde VARCHAR(9),
    numero_factura_hasta VARCHAR(9),
    estado VARCHAR(1) CHECK (estado IN ('P', 'V', 'R'))
);



CREATE TABLE DetalleFactura (
    id_detallefactura SERIAL PRIMARY KEY,
    id_factura INTEGER REFERENCES Factura(id_factura),
    cantidad NUMERIC(10, 2) NOT NULL,
    precio_unitario NUMERIC(10, 2) NOT NULL,
    descuento NUMERIC(10, 2) DEFAULT 0,
    valor NUMERIC(10, 2) NOT NULL,
	id_producto INTEGER REFERENCES Producto(id_producto),
	id_combo INTEGER REFERENCES Combo(id_combo),
	id_promocion INTEGER REFERENCES Promociones(id_promocion)
);


CREATE TABLE NotaCredito (
    id_NotaCredito SERIAL PRIMARY KEY,
    id_Factura INTEGER REFERENCES Factura(id_factura) NOT NULL,
    FechaEmision TIMESTAMP NOT NULL,
    Motivo VARCHAR(500),
    Estado CHAR(1) CHECK (Estado IN ('A', 'C'))
);

CREATE TABLE MovimientoInventario (
    id_MovimientoInventario SERIAL PRIMARY KEY,
    id_Cuenta INTEGER REFERENCES Cuenta(id_Cuenta) NOT NULL,
    id_pedido INTEGER REFERENCES Pedidos(id_Pedido),
	id_pedidoproveedor INTEGER REFERENCES pedidosproveedor(id_pedidoproveedor),
    id_bodega INTEGER REFERENCES Bodegas(id_Bodega),
    observacion VARCHAR(500),
    fechaHora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipoMovimiento CHAR(1) CHECK (tipoMovimiento IN ('E', 'S', 'P','R')) NOT NULL,
    SEstado CHAR(1) CHECK (SEstado IN ('0', '1')) NOT NULL
);

CREATE TABLE DetalleMovimientoInventario (
    id_DetalleMovimiento SERIAL PRIMARY KEY,
    id_MovimientoInventario INTEGER REFERENCES MovimientoInventario(id_MovimientoInventario) NOT NULL,
    id_Articulo INTEGER REFERENCES Componente(id_Componente),
    id_Producto INTEGER REFERENCES Producto(id_Producto),
    cantidad NUMERIC(9,2) NOT NULL,
    tipo CHAR(1) CHECK (tipo IN ('E', 'S','R')) NOT NULL
);

CREATE TABLE ReversionMovimientoInventario (
    id_Reversion SERIAL PRIMARY KEY,
    id_MovimientoInventario INTEGER REFERENCES MovimientoInventario(id_MovimientoInventario) NOT NULL,
    id_Cuenta INTEGER REFERENCES Cuenta(id_Cuenta) NOT NULL,
    fechaHora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    motivo VARCHAR(255)
);

-- Crear la tabla Tipopago
CREATE TABLE Tipopago (
	id_Tipopago SERIAL PRIMARY KEY,
    IdEmpresa INTEGER REFERENCES Empresa(id_Empresa) NOT NULL,
    Rol CHAR(1) CHECK (Rol IN ('X', 'M', 'D')) NOT NULL,
    TipoPago CHAR(1) CHECK (TipoPago IN ('H', 'S', 'T', 'M')) NOT NULL,
	cantidad NUMERIC(8, 2) NOT NULL
);

-- Crear la tabla Periodo
CREATE TABLE Periodo (
	id_Periodo SERIAL PRIMARY KEY,
    Rol CHAR(1) CHECK (Rol IN ('X', 'M', 'D')) NOT NULL,
    Desde TIMESTAMP NOT NULL,
    Hasta TIMESTAMP NOT NULL
);

-- Crear la tabla Pagos
CREATE TABLE Pagos (
	id_Pago SERIAL PRIMARY KEY,
    idEmpleado INTEGER REFERENCES Cuenta(id_Cuenta) NOT NULL,
    cantidad NUMERIC(8, 2) NOT NULL,
    TipoPago CHAR(1) CHECK (TipoPago IN ('H', 'S', 'T', 'M')) NOT NULL,
    idPeriodo INTEGER REFERENCES Periodo(id_Periodo) NOT NULL,
    HoraDePago TIMESTAMP NOT NULL
);

CREATE TABLE Codigoautorizacion (
    id_codigosauto SERIAL PRIMARY KEY,
    id_administrador INTEGER REFERENCES Administrador(id_administrador),
    codigo_autorizacion VARCHAR(49),
    fecha_vencimiento DATE,
    fecha_autorizacion DATE,
    ruc VARCHAR(13),
    nombre VARCHAR(255)
);

CREATE TABLE Codigosri (
    id_codigosri SERIAL PRIMARY KEY,
    id_administrador INTEGER REFERENCES Administrador(id_administrador),
    numero_factura_desde VARCHAR(9),
    numero_factura_hasta VARCHAR(9),
    rango_desde VARCHAR(9),
    rango_hasta VARCHAR(9),
    UNIQUE (numero_factura_desde, numero_factura_hasta)
);

CREATE TABLE Datos_Bancarios (
    id_Cuenta SERIAL PRIMARY KEY,
    Nombre_banco VARCHAR(100),
    tipo_cuenta VARCHAR(50),
    num_cuenta VARchar(100),
    nombreapellidos VARCHAR(100),
    identificacion VARCHAR(100), 
    correoelectronico VARCHAR(256)
);
