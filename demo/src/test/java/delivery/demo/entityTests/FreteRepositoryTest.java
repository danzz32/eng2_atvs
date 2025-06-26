package delivery.demo.entityTests;

import delivery.demo.model.Cidade;
import delivery.demo.model.Cliente;
import delivery.demo.model.Frete;
import delivery.demo.repository.CidadeRepository;
import delivery.demo.repository.ClienteRepository;
import delivery.demo.repository.FreteRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.util.List;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

@ActiveProfiles("test")
@DataJpaTest
public class FreteRepositoryTest {
    @Autowired
    private FreteRepository freteRepository;

    @Autowired
    private CidadeRepository cidadeRepository;

    @Autowired
    private ClienteRepository clienteRepository;

    @Test
    @DisplayName("Deve salvar o frete e buscar por cliente ordenado por valor")
    void deveBuscarFretesPorClienteOrdenadoPorValor() {
        Cliente cliente = clienteRepository.save(new Cliente("Marcos", "19821892", "Rua ABC"));
        Cidade cidade = cidadeRepository.save(new Cidade("São Luís", "MA", 15.0));

        Frete f1 = freteRepository.save(new Frete(cliente, cidade, "Entrega 1", 2.0, 12.0));
        Frete f2 = freteRepository.save(new Frete(cliente, cidade, "Entrega 2", 5.0, 10.5));

        List<Frete> fretes = freteRepository.findByClienteIdOrderByValorDesc(cliente.getId());

        assertThat(fretes).hasSize(2);

        assertThat(fretes.get(0).getValor()).isEqualTo(12.0);
        assertThat(fretes.get(1).getValor()).isEqualTo(10.5);
    }
}
