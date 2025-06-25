package delivery.demo.service;


import delivery.demo.model.Cidade;
import delivery.demo.model.Cliente;
import delivery.demo.model.Frete;
import delivery.demo.repository.CidadeRepository;
import delivery.demo.repository.ClienteRepository;
import delivery.demo.repository.FreteRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
@RequiredArgsConstructor
public class FreteService {

    private final FreteRepository freteRepository;
    private final ClienteRepository clienteRepository;
    private final CidadeRepository cidadeRepository;
    private static final double VALOR_FIXO = 10;

    public List<Frete> listarTodos() {
        return freteRepository.findAll();
    }

    public Optional<Frete> buscarPorId(Long id) {
        return freteRepository.findById(id);
    }

    public Frete salvar(Frete frete) {
        // VALIDA A EXISTÊNCIA DO CLIENTE
        Cliente cliente = clienteRepository.findById(frete.getCliente().getId())
                .orElseThrow(() -> new IllegalArgumentException("Cliente não encontrado"));

        // VALIDA A EXISTÊNCIA DA CIDADE
        Cidade cidade = cidadeRepository.findById(frete.getCidade().getId())
                .orElseThrow(() -> new IllegalArgumentException("Cidade não encontrada!"));

        // CALCULAR O VALOR DO FRETE
        double valorDoFrete = frete.getPeso() * VALOR_FIXO + frete.getCidade().getTaxa();
        frete.setValor(valorDoFrete);
        frete.setCidade(cidade);
        frete.setCliente(cliente);

        return freteRepository.save(frete);
    }

    public void deletar(Long id) {
        freteRepository.deleteById(id);
    }

    public List<Frete> buscarPorCliente(Long clienteId) {
        return freteRepository.findByClienteIdOrderByValorDesc(clienteId);
    }

    public List<Frete> buscarPorCidade(Long cidadeId) {
        return freteRepository.findByCidadeId(cidadeId);
    }

    public Optional<Frete> freteComMaiorValor() {
        return freteRepository.findAll().stream().max(Comparator.comparingDouble(Frete::getValor));
    }

    public Optional<Cidade> cidadeComMaisFretes() {
        List<Frete> fretes = freteRepository.findAll();
        Map<Cidade, Long> contagem = new HashMap<>();

        for (Frete frete : fretes) {
            contagem.put(frete.getCidade(), contagem.getOrDefault(frete.getCidade(), 0L) + 1);
        }

        return contagem.entrySet()
                .stream()
                .max(Map.Entry.comparingByValue())
                .map(Map.Entry::getKey);
    }

}

