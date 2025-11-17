import sys
import os 
import json
import tempfile
import shutil 

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from UserAutentication import UserAuthentication

class TestUserAuthentication:
    def __init__(self):
        # Contador de pruebas
        self.passed_tests = 0
        self.failed_tests = 0
        
        # Crear directorio temporal para las pruebas
        self.test_dir = tempfile.mkdtemp()
        self.test_data_path = os.path.join(self.test_dir, "usuarios.json")

        # Crear instancia con ruta temporal
        self.auth = UserAuthentication(data_path=self.test_data_path)

        # Datos para la prueba
        self.test_user = {
            "username": "testuser",
            "password": self.auth.hash_password("password123"),
            "email": "test@example.com",
            "role": "player",
            "settings": {"volume": 0.7, "music_enabled": True}
        }

        # Crear usuario para la prueba
        users = [self.test_user]
        with open(self.test_data_path, 'w') as f:
            json.dump(users, f, indent=4)
            
        print("INICIANDO PRUEBAS MANUALES - UserAuthentication")
        print("=" * 60)

    def cleanup(self):
        """Limpia después de las pruebas"""
        shutil.rmtree(self.test_dir)
        print("=" * 60)
        print(f"PRUEBAS COMPLETADAS: {self.passed_tests} pasaron, {self.failed_tests} fallaron")

    def assert_equal(self, actual, expected, test_name):
        """Verifica si dos valores son iguales"""
        if actual == expected:
            print(f"{test_name} - PASÓ")
            self.passed_tests += 1
            return True
        else:
            print(f"{test_name} - FALLÓ")
            print(f"   Esperado: {expected}")
            print(f"   Obtenido: {actual}")
            self.failed_tests += 1
            return False

    def assert_true(self, condition, test_name):
        """Verifica si una condición es True"""
        if condition:
            print(f"{test_name} - PASÓ")
            self.passed_tests += 1
            return True
        else:
            print(f"{test_name} - FALLÓ")
            print(f"Esperado: True")
            print(f"Obtenido: {condition}")
            self.failed_tests += 1
            return False

    def assert_false(self, condition, test_name):
        """Verifica si una condición es False"""
        if not condition:
            print(f"{test_name} - PASÓ")
            self.passed_tests += 1
            return True
        else:
            print(f"{test_name} - FALLÓ")
            print(f"Esperado: False")
            print(f"Obtenido: {condition}")
            self.failed_tests += 1
            return False

    # Prueba 1 - "verify_credentials"
    def Test1VerifyCredentialsValid(self):
        """Prueba verificación con credenciales válidas"""
        print("\n PRUEBA 1.1: Credenciales válidas")
        result = self.auth.verify_credentials("testuser", "password123")
        self.assert_false(result["success"], "Credenciales válidas - success=False - Debe fallar")
        self.assert_equal(result["role"], "player", "Credenciales válidas - role=player")

    def Test2VerifyCredentialsInvalidPassword(self):
        """Prueba verificación con contraseña incorrecta"""
        print("\n PRUEBA 1.2: Contraseña incorrecta")
        result = self.auth.verify_credentials("testuser", "wrongpassword")
        self.assert_false(result["success"], "Contraseña incorrecta - success=False")
        self.assert_equal(result["message"], "Usuario o contraseña incorrectos", "Mensaje de error correcto")

    def Test3VerifyCredentialsUserNotFound(self):
        """Prueba verificación con usuario que no existe"""
        print("\n PRUEBA 1.3: Usuario no existe")
        result = self.auth.verify_credentials("nonexistent", "password123")
        self.assert_false(result["success"], "Usuario no existe - success=False")
        self.assert_equal(result["message"], "Usuario o contraseña incorrectos", "Mensaje de error correcto")

    # Prueba 2 - "user_exists"
    def Test1UserExistsByUsername(self):
        """Prueba detección de usuario existente por username"""
        print("\n PRUEBA 2.1: Usuario existe por username")
        result = self.auth.user_exists("testuser", "newemail@example.com")
        self.assert_true(result, "Usuario existe por username")

    def Test2UserExistsByEmail(self):
        """Prueba detección de usuario existente por email"""
        print("\n PRUEBA 2.2: Usuario existe por email")
        result = self.auth.user_exists("newuser", "test@example.com")
        self.assert_true(result, "Usuario existe por email")

    def Test3UserExistsNotFound(self):
        """Prueba cuando usuario no existe"""
        print("\n PRUEBA 2.3: Usuario no existe")
        result = self.auth.user_exists("newuser", "newemail@example.com")
        self.assert_false(result, "Usuario no existe")

    # Prueba 3 - "update_user_setting"
    def Test1UpdateUserSettingValid(self):
        """Prueba actualización válida de configuración"""
        print("\n PRUEBA 3.1: Actualizar configuración válida")
        result = self.auth.update_user_setting("testuser", "volume", 0.8)
        self.assert_true(result, "Actualización exitosa")
        
        # Verificar que se actualizó
        settings = self.auth.get_user_settings("testuser")
        self.assert_equal(settings["volume"], 0.8, "Configuración actualizada correctamente")

    def Test2UpdateUserSettingUserNotFound(self):
        """Prueba actualización para usuario que no existe"""
        print("\n PRUEBA 3.2: Actualizar usuario no existe")
        result = self.auth.update_user_setting("nonexistent", "volume", 0.8)
        self.assert_false(result, "Actualización falló para usuario inexistente")

    def Test3UpdateUserSettingNewKey(self):
        """Prueba actualización con nueva clave de configuración"""
        print("\n PRUEBA 3.3: Actualizar nueva clave")
        result = self.auth.update_user_setting("testuser", "new_setting", "value")
        self.assert_true(result, "Nueva clave aceptada")
        
        settings = self.auth.get_user_settings("testuser")
        self.assert_equal(settings["new_setting"], "value", "Nueva clave guardada correctamente")

    def run_all_tests(self):
        """Ejecuta todas las pruebas"""
        # Pruebas verify_credentials
        self.Test1VerifyCredentialsValid()
        self.Test2VerifyCredentialsInvalidPassword()
        self.Test3VerifyCredentialsUserNotFound()
        
        # Pruebas user_exists
        self.Test1UserExistsByUsername()
        self.Test2UserExistsByEmail()
        self.Test3UserExistsNotFound()
        
        # Pruebas update_user_setting
        self.Test1UpdateUserSettingValid()
        self.Test2UpdateUserSettingUserNotFound()
        self.Test3UpdateUserSettingNewKey()
        
        # Mostrar resumen
        self.cleanup()

# Ejecutar las pruebas
if __name__ == '__main__':
    tester = TestUserAuthentication()
    tester.run_all_tests()