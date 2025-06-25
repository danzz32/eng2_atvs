package delivery.demo.repository;


import delivery.demo.model.Cidade;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface CidadeRepository extends JpaRepository<Cidade, Long> {

    // READ
    List<Cidade> findAll();

    Optional<Cidade> findById(Long id);

    // CREATE / UPDATE
    Cidade save(Cidade cidade);

    // DELETE
    void deleteById(Long id);

    // Custom (exemplo)
    List<Cidade> findByUf(String uf);

    List<Cidade> findByNomeContainingIgnoreCase(String nome);
}

