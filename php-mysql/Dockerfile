# Usa la versión de PHP que necesites (por ejemplo, PHP 7.4)
FROM php:7.4-fpm

# Copia tu código PHP a la carpeta de trabajo en el contenedor
COPY . /var/www/html

# Instala extensiones de PHP y herramientas necesarias
RUN apt-get update && \
    apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) gd pdo pdo_mysql

# Expon el puerto en el que PHP-FPM está escuchando
EXPOSE 9000

CMD ["php-fpm"]
