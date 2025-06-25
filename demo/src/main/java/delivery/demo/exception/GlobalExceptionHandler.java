package delivery.demo.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.validation.ObjectError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, String>> handleValidationErrors(MethodArgumentNotValidException e) {
        Map<String, String> erros = new HashMap<>();

        for (ObjectError erro : e.getBindingResult().getAllErrors()) {
            String campo = ((FieldError) erro).getField();
            String mensagem = erro.getDefaultMessage();

            erros.put(campo, mensagem);
        }
        return new ResponseEntity<>(erros, HttpStatus.BAD_REQUEST);
    }
}
