# Implementasi FTP dengan Fitur Keamanan

**Pertama, untuk menggunakan server ini, Anda harus membuat sertifikat SSL terlebih dahulu.**
- Berikut ini adalah perintah untuk menghasilkan _self-signed certificate_ pada Terminal/Command Prompt **(CMD)**:

```sh
openssl req -x509 -nodes -out server.crt -keyout server.key
```
> :warning: **Apabila belum ter-install:** bisa jalankan melalui Git Bash bisa diinstal di [sini](https://git-scm.com/download/win).
