package delivery.demo.controller;


import delivery.demo.model.Frete;
import delivery.demo.service.FreteService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/fretes")
@RequiredArgsConstructor
public class FreteController {

    private final FreteService freteService;

    @GetMapping
    public List<Frete> listarTodos() {
        return freteService.listarTodos();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Frete> buscarPorId(@PathVariable Long id) {
        return freteService.buscarPorId(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Frete> criar(@Valid @RequestBody Frete frete) {
        Frete novo = freteService.salvar(frete);
        return ResponseEntity.ok(novo);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletar(@PathVariable Long id) {
        freteService.deletar(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/cliente/{clienteId}")
    public List<Frete> buscarPorCliente(@PathVariable Long clienteId) {
        return freteService.buscarPorCliente(clienteId);
    }

    @GetMapping("/cidade/{cidadeId}")
    public List<Frete> buscarPorCidade(@PathVariable Long cidadeId) {
        return freteService.buscarPorCidade(cidadeId);
    }
}

