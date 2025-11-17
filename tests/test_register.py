from Register import UserRegistration

def test1ValidatePassword_Correcta():
    v = UserRegistration()
    errors = v.ValidatePassword("Abcdef123456!!")
    assert len(errors) == 0   # No debe haber errores

def test2ValidatePassword_MuyCorta():
    v = UserRegistration()
    errors = v.ValidatePassword("Abc1!")
    assert "La contraseña debe tener al menos 12 caracteres." in errors

def test3ValidatePassword_SinMayuscula():
    v = UserRegistration()
    errors = v.ValidatePassword("abcdef123456!!")
    assert "Debe contener al menos una letra mayúscula." in errors
