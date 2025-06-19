package delivery.demo.service;


import delivery.demo.model.Frete;
import delivery.demo.repository.FreteRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class FreteService {

    private final FreteRepository freteRepository;

    public List<Frete> listarTodos() {
        return freteRepository.findAll();
    }

    public Optional<Frete> buscarPorId(Long id) {
        return freteRepository.findById(id);
    }

    public Frete salvar(Frete frete) {
        return freteRepository.save(frete);
    }

    public void deletar(Long id) {
        freteRepository.deleteById(id);
    }

    public List<Frete> buscarPorCliente(Long clienteId) {
        return freteRepository.findByClienteId(clienteId);
    }

    public List<Frete> buscarPorCidade(Long cidadeId) {
        return freteRepository.findByCidadeId(cidadeId);
    }
}

