package delivery.demo.repository;


import delivery.demo.model.Frete;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface FreteRepository extends JpaRepository<Frete, Long> {

    // READ
    List<Frete> findAll();

    Optional<Frete> findById(Long id);

    // CREATE / UPDATE
    Frete save(Frete frete);

    // DELETE
    void deleteById(Long id);

    // Custom (exemplo)
    List<Frete> findByCidadeId(Long cidadeId);

    List<Frete> findByClienteIdOrderByValorDesc(Long clienteId);
}

