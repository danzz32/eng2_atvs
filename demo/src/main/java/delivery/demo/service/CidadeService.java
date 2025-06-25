package delivery.demo.service;


import delivery.demo.model.Cidade;
import delivery.demo.repository.CidadeRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class CidadeService {

    private final CidadeRepository cidadeRepository;

    public List<Cidade> listarTodas() {
        return cidadeRepository.findAll();
    }

    public Optional<Cidade> buscarPorId(Long id) {
        return cidadeRepository.findById(id);
    }

    public Cidade salvar(Cidade cidade) {
        return cidadeRepository.save(cidade);
    }

    public void deletar(Long id) {
        cidadeRepository.deleteById(id);
    }

    public List<Cidade> buscarPorUf(String uf) {
        return cidadeRepository.findByUf(uf);
    }

    public List<Cidade> buscarPorNome(String nome){
        return cidadeRepository.findByNomeContainingIgnoreCase(nome);
    }
}

